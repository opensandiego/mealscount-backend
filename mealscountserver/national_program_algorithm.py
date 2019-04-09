# coding: utf-8

# MealsCount Algorithm (v2)
import sys
import pandas as pd
import numpy as np
import time
import math
import abc
from pathlib import Path
import arrow

from mealscountserver.backend_utils import prepare_data
from . import backend_utils as bu
from . import national_rates_config_parser as cp

from config import *


class mcAlgorithm(metaclass=abc.ABCMeta):
    """
    Base class for the MealsCount Algorithm.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def version(self):
        pass

    @abc.abstractmethod
    def get_school_groupings(self, data, bundle_groups=False):
        pass

    # @abc.abstractmethod
    # def get_school_groups(self, data):
    #     pass


class CEPSchoolGroupGenerator:
    """
    Class to encapsulate data and operations for grouping schools.
    """

    def __init__(self, cfg=None, strategy=None):
        if strategy and cfg and isinstance(cfg, dict):  # and hasattr(strategy, 'get_school_groupings'):
            self.strategy = strategy
            self.config = cfg
        else:
            raise ValueError("ERROR: Invalid inputs")

    def get_groups(self, school_data):
        """get_school_groupings yields a series with each group with a unique int in column"""

        yield from self.strategy.get_school_groupings(school_data, format)

    def get_group_bundles(self, school_data):

        results = None
        try:
            algo = self.strategy

            if algo.run(school_data, self.config, bundle_groups=True):
                results = list(algo.get_school_groups(school_data, format))
            else:
                s = "ERROR: Failed to generate school groups"
                print(s)
            yield from (x for x in results)
        except Exception as e:
            raise e


#
# Utility function to truncate a float (f) to the specified number (n) of
# decimals without rounding
#
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


#
# Function to generate summary data for the specified group of schools
#
def summarize_group(group_df):
    """compute total eligible and total enrolled students across all schools in the group"""
    summary = group_df[['total_enrolled', 'direct_cert', 'non_direct_cert', 'total_eligible']].aggregate(['sum'])
    # compute the group's ISP
    summary = summary.assign(grp_isp=(summary['total_eligible'] / summary['total_enrolled']) * 100)
    # count the number of schools in the group
    summary = summary.assign(size=group_df.shape[0])
    # compute the % of meals covered at the free and paid rate for the group's ISP
    grp_isp = summary.loc['sum', 'grp_isp']
    free_rate = (grp_isp * 1.6) if grp_isp >= (funding_rules['min_cep_thold_pct'] * 100) else 0.0
    free_rate = 100. if free_rate > 100. else free_rate
    summary = summary.assign(free_rate=free_rate)
    paid_rate = (100.0 - free_rate)
    summary = summary.assign(paid_rate=paid_rate)

    return summary


#
# Function to select schools to add, from among all schools not already in the destination group (df),
# to the destination group (whose summary is provided as input) based on the impact each school has on the
# destination group's ISP. Target ISP specifies the desired ISP at which to maintain the destination group
#
def select_by_isp_impact(df, group_df, target_isp):
    schools_to_add = pd.DataFrame()

    dst_grp_total_enrolled = group_df.loc[:, 'total_enrolled'].sum()
    dst_grp_total_eligible = group_df.loc[:, 'total_eligible'].sum()

    new_total_enrolled = df.loc[:, 'total_enrolled'] + dst_grp_total_enrolled
    new_isp = (((df.loc[:, 'total_eligible'] + dst_grp_total_eligible) / new_total_enrolled) * 100).astype(np.double)

    isp_impact = pd.DataFrame({'new_isp': new_isp})
    isp_impact.sort_values('new_isp', ascending=False, inplace=True)

    # select all schools whose ISP impact is small enough to not bring down the new ISP
    # to under the target ISP
    idx = isp_impact[isp_impact['new_isp'] >= target_isp].index
    if len(idx) > 0:

        # add them to the existing group temporarily
        tmp_group_df = pd.concat([group_df, df.loc[idx, :]], axis=0)

        # recompute cumulative isp
        cum_isp = (tmp_group_df['total_eligible'].cumsum() / tmp_group_df['total_enrolled'].cumsum()).astype(
            np.double) * 100
        tmp_group_df.loc[:, 'cum_isp'] = cum_isp

        # retain only those that make the cut
        bins = [0., target_isp, 100.]
        tmp_groups = tmp_group_df.groupby(pd.cut(tmp_group_df['cum_isp'], bins))
        ivals = tmp_groups.size().index.tolist()
        tmp_df = tmp_groups.get_group(ivals[-1]).apply(list).apply(pd.Series)

        # determine which subset of schools to actully add
        potential_additions = idx
        group_selections = tmp_df.index.tolist()
        actual_additions = []
        for x in potential_additions:
            if x in group_selections:
                actual_additions.append(x)

        # generate schools to add
        if (len(actual_additions)):
            schools_to_add = df.loc[actual_additions, :]

    return schools_to_add


#
# Function to take in school data and group them based on the ISP_WIDTH
#
def groupby_isp_width(df, target_isp_width=None):
    min_cep_thold = (funding_rules['min_cep_thold_pct'] * 100)

    # use default ISP width if not specified as  input
    isp_width = model_version_info['isp_width_default'] if target_isp_width is None else target_isp_width

    # recalculate cumulative-isp
    df['cum_isp'] = (df['total_eligible'].cumsum() / df['total_enrolled'].cumsum()).astype(np.double) * 100

    top_isp = df.iloc[0]['isp']

    # if the top ISP is less than that needed for CEP eligibility
    # we have nothing more to do
    if top_isp < min_cep_thold:
        return None

    # determine the next cut-off point
    isp_thold = (top_isp - isp_width) if (top_isp - isp_width) >= min_cep_thold else min_cep_thold

    # group schools at the cut-off point
    # note that this will generate exactly 2 groups: one of length ISP_WIDTH and the other containing
    # the rest of the schools
    groups = df.groupby(pd.cut(df['cum_isp'], [0., isp_thold, top_isp]))

    return groups


#
# Function that implements a strategy to group schools with ISPs lower than that needed for
# 100% CEP funding.
#
def group_schools_low_isp(df, isp_width=None):
    # school_groups = []
    # school_group_summaries = []

    top_isp = df.iloc[0]['isp']

    # exit the loop if the highest ISP from among the remaining schools (which are sorted by ISP)
    # is lower than that needed for CEP eligibility; we have nothing more to do

    while top_isp >= (funding_rules['min_cep_thold_pct'] * 100):

        # get the next isp_width group that still qualifies for CEP
        groups = groupby_isp_width(df, isp_width)

        if (groups != None):

            ivals = pd.DataFrame(groups.size()).index.tolist()

            # get the last group: this is the group of isp_width
            group_df = groups.get_group(ivals[-1])
            # summary_df = summarize_group(group_df)

            # trim the school data to remove this group
            df.drop(group_df.index.tolist(), axis=0, inplace=True)
            # from among remaining schools see if any qualify based on isp impact
            schools_to_add = select_by_isp_impact(df, group_df, (funding_rules['max_cep_thold_pct'] * 100))

            if schools_to_add.shape[0] > 0:
                group_df = pd.concat([group_df, schools_to_add], axis=0)
                df.drop(schools_to_add.index.tolist(), axis=0, inplace=True)
            yield group_df
            # school_groups.append(group_df)
            #
            # summary_df = summarize_group(group_df)
            # school_group_summaries.append(summary_df)

            # get the top isp for the remaining schools
            top_isp = df.iloc[0]['isp']

            # at this point all remaining schools are ineligible for CEP
    # pass them along as a group of their own
    cum_isp = (df['total_eligible'].cumsum() / df['total_enrolled'].cumsum()).astype(np.double) * 100
    df = df.assign(cum_isp=cum_isp)

    # summary_df = summarize_group(df)
    # school_group_summaries.append(summary_df)

    yield df


#
# Function that implements a strategy to group schools with ISPs higher than (or equal to)
# that needed for 100% CEP funding.
#
def group_schools_high_isp(df):
    """partitions the df based on max_cep_thold_pct"""
    # school_groups = []
    # school_group_summaries = []

    # group the data by cumulative ISP such that all schools with
    # max CEP threshold and higher are part of a single group; the
    # rest of the schools are in a second group

    bins = [-1., funding_rules['max_cep_thold_pct'] * 100, 100.]
    return df.groupby(pd.cut(df['cum_isp'], bins)).ngroup(ascending=True)
    # groups = df.groupby(pd.cut(df['cum_isp'], bins))
    # ivals = groups.size().index.tolist()
    #
    # group_df = groups.get_group(ivals[-1]).apply(list).apply(pd.Series)
    # summary_df = summarize_group(group_df, cfg)

    # df.drop(group_df.index.tolist(), axis=0, inplace=True)
    # # from among remaining schools see if any qualify based on isp impact
    # schools_to_add = select_by_isp_impact(df, group_df, (cfg.max_cep_thold_pct() * 100))
    #
    # if schools_to_add.shape[0] > 0:
    #     group_df = pd.concat([group_df, schools_to_add], axis=0)
    #     df.drop(schools_to_add.index.tolist(), axis=0, inplace=True)
    #
    # school_groups.append(group_df)
    #
    # summary_df = summarize_group(group_df, cfg)
    # school_group_summaries.append(summary_df)
    #
    # return school_groups, school_group_summaries


def show_results(groups, summaries):
    n = len(groups)

    for i in range(n):
        print('GRP {}'.format(i))
        print(summaries[i])
        print(groups[i])

    return


#
# Function to prepare school group and summary data in JSON format
#
def prepare_results_json(df, metadata, ts, target_isp_width=None):
    isp_grp = df.groupby(['group_isp'])

    # use default ISP width if not specified as  input
    isp_width = model_version_info['isp_width'] if target_isp_width is None else target_isp_width

    json_result = {}

    # use default ISP width if not specified as  input
    isp_width = model_version_info['isp_width'] if target_isp_width is None else target_isp_width

    n = len(isp_grp)

    json_result['lea'] = metadata['lea']
    json_result['academic_year'] = metadata['academic_year']
    json_result['timestamp'] = ts

    groups_dl = []
    for group_df in isp_grp:
        g = summaries[i]

        eligibility = 'yes' if g.loc['sum', 'grp_isp'] >= (cfg['min_cep_thold_pct'] * 100) else 'no'
        schools = groups[i].loc[:, 'school_code'].values.tolist()

        # json does not serialize numpy types. convert them to native ones below

        g_json = {"group": i,
                  "eligible_for_cep": eligibility,
                  "total_enrolled": int(g.loc['sum', 'total_enrolled']),
                  "direct_cert": int(g.loc['sum', 'direct_cert']),
                  "non_direct_cert": int(g.loc['sum', 'non_direct_cert']),
                  "total_eligible": int(g.loc['sum', 'total_eligible']),
                  "group_isp": truncate(float(g.loc['sum', 'grp_isp']), 2),
                  "group_size": int(g.loc['sum', 'size']),
                  "schools": schools}

        groups_dl.append(g_json)

    json_result['school_groups'] = {"num_groups": n, "group_summaries": groups_dl}
    json_result['mealscount_config_version'] = model_version_info['version']
    json_result['model_params'] = {'model_variant': model_version_info['model_variant'], 'isp_width': isp_width}

    # print(json_result)

    return json_result


#
# Function to return school group and summary data as html string
#
def monthly_federal_funds(data):
    """calculates the monthly federal funds a school receives."""

    rates = pd.Series([x for x in config['model_params']['cep_rates'] if x['region'] == "default"][0])
    # data['group'] = np.NaN

    data['eligible'] = np.where((data.grp_isp / 100) < cfg['min_cep_thold_pct'], 0, 1)
    data['govt_funding_level'] = np.where(data.grp_isp * 1.6 > 100, 1, data.grp_isp * 1.6 / 100)

    # data.sort_values(['grp_isp', 'isp_students'],
    #                  ascending=[False, False],
    #                  inplace=True)
    # assert set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes)) == set(), \
    #     "the 2 groups intersect: {}".format(data.iloc[set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes))].to_html())

    # assistance = 0.06 * (True|False)
    assistance = cfg['performance_based_cash_assistance_per_lunch'] * cfg['assistance']

    data['federal_money_per_student_per_day'] = \
        data.govt_funding_level * (rates.nslp_lunch_free_rate + assistance) * data.eligible + \
        (1 - data.govt_funding_level) * (rates.nslp_lunch_paid_rate + assistance) * data.eligible + \
        data.govt_funding_level * rates.sbp_bkfst_free_rate * data.eligible + \
        (1 - data.govt_funding_level) * rates.sbp_bkfst_paid_rate * data.eligible
    data['federal_money_per_month'] = data['federal_money_per_student_per_day'] * data.total_enrolled * \
                                      cfg['monthly_lunches'] * data.govt_funding_level
    return data


# def prepare_results_html(df, metadata, ts, target_isp_width=None, form=None):
#     isp_grp = df.groupby(['group_isp'])
#
#     # use default ISP width if not specified as  input
#     isp_width = model_version_info['isp_width'] if target_isp_width is None else target_isp_width
#
#     html_result = ""
#
#
#     n = len(groups)
#
#     html_result += """<table border="1">"""
#     html_result += "<tr><td><b>LEA</b>: {}</td>".format(metadata['lea'])
#     html_result += "<td><b>Academic Year</b>: {}</td>".format(metadata['academic_year'])
#
#     html_result += "<td><b>Timestamp</b>: {}</td></tr>".format(ts)
#     html_result += "</table>"
#
#     # html_result += "<br>"
#     # html_result += """<table border="1">"""
#     # html_result += "<tr><td><b>Num Groups</b>: {}</td><tr>".format(n)
#     # html_result += "</table>"
#     # html_result += "<br>"
#
#     html_result += """<table border="1">"""
#     html_result += "<tr><th>Group</th><th>CEP Eligibility</th><th>Total Enrolled</th><th>Direct Certified</th>"
#     html_result += "<th>Non-Direct Certified</th><th>Total Eligible</th><th>Group ISP</th><th>Group Size</th>"
#     html_result += "<th>Schools</th>"
#     html_result += "<th>Federal Monthly Funds (with 100% participation)</th>"
#     html_result += "<th>federal_money_per_student_per_day</th>"
#
#
#
#     groups_dl = []
#     for i in range(n):
#         g = summaries[i]
#
#         eligibility = 'yes' if g.loc['sum', 'grp_isp'] >= (cfg['min_cep_thold_pct'] * 100) else 'no'
#         schools = groups[i].loc[:, 'school_code'].values.tolist()
#
#         html_result += "<tr><td>{}</td><td>{}</td><td>{}</td>".format(i, eligibility,
#                                                                       int(g.loc['sum', 'total_enrolled']))
#         html_result += "<td>{}</td><td>{}</td><td>{}</td>".format(int(g.loc['sum', 'direct_cert']),
#                                                                   int(g.loc['sum', 'non_direct_cert']),
#                                                                   int(g.loc['sum', 'total_eligible']))
#         html_result += "<td>{}</td><td>{}</td><td>{}</td>".format(truncate(float(g.loc['sum', 'grp_isp']), 2),
#                                                                   int(g.loc['sum', 'size']),
#                                                                   ", ".join([str(s) for s in schools]))
#         data = monthly_federal_funds(g.loc['sum'], cfg)
#         html_result += "<td>{0:.2f}</td>".format(data.federal_money_per_month)
#         html_result += "<td>{0:.2f}</td>".format(data.federal_money_per_student_per_day)
#         html_result += "</tr>"
#
#     html_result += "</table>"
#     # html_result += "<br>"
#
#     html_result += """<table border="1">"""
#     html_result += "<tr><td><b>MealsCount Config Version</b>: {}</td>".format(cfg.version())
#     html_result += "<td><b>Model Variant</b>: {}</td><td><b>ISP Width</b>: {}</td></tr>".format(cfg.model_variant(),
#                                                                                                 isp_width)
#
#     html_result += "</table>"
#
#     # print(html_result)
#
#     return html_result


class mcAlgorithmV2(mcAlgorithm):
    """
    Implementation of the MealsCount Algorithm variant V2
    """

    def __init__(self):
        pass

    def version(self):
        return "v2"

    def get_school_groupings(self, data, bundle_groups=False):
        """ This yields series of school groupings """

        df = data.to_frame()
        # df = prepare_data(df)

        # g1, s1 = group_schools_high_isp(df, cfg)
        high = group_schools_high_isp(df)

        results_ts = arrow.now().isoformat()

        if not bundle_groups:
            # g2, s2 = group_schools_low_isp(df, cfg)
            df2 = group_schools_low_isp(df)
            # self.json_results = prepare_results_json(g1 + g2, s1 + s2, cfg, md, results_ts)
            # self.html_results = prepare_results_html(g1 + g2, s1 + s2, cfg, md, results_ts)
        else:
            isp_width_bundle = model_version_info['isp_width_bundle']

            for isp_width in isp_width_bundle:
                g = group_schools_low_isp(df, isp_width)
                # json_list.append(prepare_results_json(g1 + g, s1 + s, cfg, md, results_ts, isp_width))
                # html_list.append(prepare_results_html(g1 + g, s1 + s, cfg, md, results_ts, isp_width))

            # self.json_results = {"bundles": json_list}
            # self.html_results = "<br><br>".join(html_list)

            # uncomment below for debugging
        # show_results(g1+g2,s1+s2)
    # return True

    # def get_school_groups(self, data):
    #     if format == "json":
    #         return self.json_results
    #     else:
    #         return self.html_results
    #


#
# MAIN
#
def main():
    CWD = Path('.')

    DATADIR = CWD.joinpath("data")
    DATAFILE = "calpads_sample_data.xlsx"
    DATAFILE_LARGE = "calpads_sample_data_large.xlsx"

    processing_times = []

    # assumes only filename is specified and that the file is present under
    # DATADIR in the current workspace
    if (len(sys.argv) > 1):
        data_file = sys.argv[1]
    else:
        data_file = DATAFILE_LARGE

    print("Processing file: {}".format(data_file))
    print(" ")
    print(" ")

    CONFIG_FILE = "national_config.json"

    cfg = cp.mcModelConfig(CONFIG_FILE)
    strategy = mcAlgorithmV2() if cfg.model_variant() == "v2" else None
    grouper = CEPSchoolGroupGenerator(cfg, strategy)

    start_t = time.time()
    data = bu.dataFrameAndMetadataFromXL(DATADIR.joinpath(data_file))
    processing_times.append(round((time.time() - start_t), 2))

    start_t = time.time()
    json_groups = grouper.get_groups(data, "json")
    processing_times.append(round((time.time() - start_t), 2))

    start_t = time.time()
    json_bundles = grouper.get_group_bundles(data, "json")
    processing_times.append(round((time.time() - start_t), 2))

    start_t = time.time()
    html_groups = grouper.get_groups(data, "html")
    processing_times.append(round((time.time() - start_t), 2))

    start_t = time.time()
    html_bundles = grouper.get_group_bundles(data, "html")
    processing_times.append(round((time.time() - start_t), 2))

    # print(json.dumps(json_groups, indent=2))
    # print(json.dumps(json_bundles, indent=2))

    # print("<html><body>{}</body></html>".format(html_groups))
    print("<html><body><br><br>{}<br></body></html>".format(html_bundles))

    print(" ")
    print("Processing times (secs): ")
    print("parse: {} json: groups ({}) bundles ({}) html: groups ({}) bundles ({})".format(processing_times[0],
                                                                                           processing_times[1],
                                                                                           processing_times[2],
                                                                                           processing_times[3],
                                                                                           processing_times[4]))


# end: main

if __name__ == "__main__":
    main()
else:
    # do nothing
    pass
