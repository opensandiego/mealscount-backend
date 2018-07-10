# coding: utf-8

# MealsCount Algorithm (v2)

import os
import pandas as pd
import numpy as np
import time
from datetime import datetime
import abc

from . import backend_utils as bu
from . import config_parser as cp


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
    def run(self, data, cfg, bundle_groups=False):
        pass

    @abc.abstractmethod
    def get_school_groups(self, data, format="json"):
        pass


class CEPSchoolGroupGenerator:
    """
    Class to encapsulate data and operations for grouping schools.
    """
    __strategy = None

    def __init__(self, cfg, strategy=None):
        if not (strategy):
            raise ValueError("ERROR: Invalid strategy")
        self.__strategy = strategy
        self.__config = cfg

    def get_groups(self, school_data, format="json"):

        results = None

        if not (self.__strategy):
            raise ValueError("ERROR: Invalid strategy")

        try:
            algo = self.__strategy
            if algo.run(school_data, self.__config):
                results = algo.get_school_groups(school_data, format)
            else:
                s = "ERROR: Failed to generate school groups"
                print(s)
            return results
        except Exception as e:
            raise e

    def get_group_bundles(self, school_data, format="json"):

        results = None

        if not (self.__strategy):
            raise ValueError("ERROR: Invalid strategy")

        try:
            algo = self.__strategy

            if algo.run(school_data, self.__config, bundle_groups=True):
                results = algo.get_school_groups(school_data, format)
            else:
                s = "ERROR: Failed to generate school groups"
                print(s)
            return results
        except Exception as e:
            raise e


#
# Function wrangle the school district input data to the necessary form to
# generate groupings of schools based on ISP
#

def prepare_data(df):
    # remove aggregated records
    df = df[df['school_name'] != 'total']

    # sum cols for homeless, migrant and foster students
    df = df.assign(non_direct_cert=(df['foster'] + df['homeless'] + df['migrant']))

    # compute total eligible and isp
    total_eligible = (df['foster'] + df['homeless'] + df['migrant'] + df['direct_cert'])
    isp = (total_eligible / df['total_enrolled']) * 100
    df = df.assign(total_eligible=total_eligible)
    df = df.assign(isp=isp)
    df.loc[:, 'isp'] = np.around(df['isp'].astype(np.double), 2)

    KEEP_COLS = ['school_code', 'total_enrolled', 'direct_cert', 'non_direct_cert', 'total_eligible', 'isp']

    # remove cols not needed for further analysis
    drop_cols = [s for s in df.columns.tolist() if s not in set(KEEP_COLS)]
    df.drop(drop_cols, axis=1, inplace=True)

    # sort by isp
    df.sort_values('isp', ascending=False, inplace=True)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)

    # compute cumulative isp
    cum_isp = np.around((df['total_eligible'].cumsum() / df['total_enrolled'].cumsum()).astype(np.double) * 100, 2)
    df = df.assign(cum_isp=cum_isp)

    return df


#
# Function to generate summary data for the specified group of schools
#
def summarize_group(group_df, cfg):
    # compute total eligible and total enrolled students across all schools in the group
    summary = group_df[['total_enrolled', 'direct_cert', 'non_direct_cert', 'total_eligible']].aggregate(['sum'])
    # compute the group's ISP
    summary = summary.assign(grp_isp=round((summary['total_eligible'] / summary['total_enrolled']) * 100, 2))
    # count the number of schools in the group
    summary = summary.assign(size=group_df.shape[0])
    # compute the % of meals covered at the free and paid rate for the group's ISP
    grp_isp = summary.loc['sum', 'grp_isp']
    free_rate = round(grp_isp * 1.6, 2) if grp_isp >= (cfg.min_cep_thold_pct() * 100) else 0.0
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
def select_by_isp_impact(df, dst_group_summary, target_isp):
    schools_to_add = pd.DataFrame()

    dst_grp_total_enrolled = dst_group_summary['total_enrolled']
    dst_grp_total_eligible = dst_group_summary['total_eligible']

    new_total_enrolled = df['total_enrolled'] + dst_grp_total_enrolled
    new_isp = np.around(
        (((df['total_eligible'] + dst_grp_total_eligible) / new_total_enrolled) * 100).astype(np.double), 2)

    tmp_df = pd.DataFrame({'new_isp': new_isp})

    # select all schools whose ISP impact is small enough to not bring down the new ISP
    # to under the target ISP
    idx = tmp_df[tmp_df['new_isp'] >= target_isp].index
    if len(idx) > 0:
        schools_to_add = df.loc[idx, :]

    return schools_to_add


#
# Function to take in school data and group them based on the ISP_WIDTH
#
def groupby_isp_width(df, cfg, target_isp_width=None):
    min_cep_thold = (cfg.min_cep_thold_pct() * 100)

    # use default ISP width if not specified as  input
    isp_width = cfg.isp_width() if target_isp_width is None else target_isp_width

    # recalculate cumulative-isp
    cum_isp = np.around((df['total_eligible'].cumsum() / df['total_enrolled'].cumsum()).astype(np.double) * 100, 2)
    df = df.assign(cum_isp=cum_isp)

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
def group_schools_lo_isp(df, cfg, isp_width=None):
    school_groups = []
    school_group_summaries = []

    top_isp = df.iloc[0]['isp']

    # exit the loop if the highest ISP from among the remaining schools (which are sorted by ISP)
    # is lower than that needed for CEP eligibility; we have nothing more to do

    while top_isp >= (cfg.min_cep_thold_pct() * 100):

        # get the next isp_width group that still qualifies for CEP
        groups = groupby_isp_width(df, cfg, isp_width)

        if (groups != None):

            ivals = pd.DataFrame(groups.size()).index.tolist()

            # get the last group: this is the group of isp_width
            group_df = groups.get_group(ivals[-1])
            summary_df = summarize_group(group_df, cfg)

            # trim the school data to remove this group
            df.drop(group_df.index.tolist(), axis=0, inplace=True)
            # from among remaining schools see if any qualify based on isp impact
            schools_to_add = select_by_isp_impact(df, summary_df, (cfg.max_cep_thold_pct() * 100))

            if schools_to_add.shape[0] > 0:
                group_df = pd.concat([group_df, schools_to_add], axis=0)
                df.drop(schools_to_add.index.tolist(), axis=0, inplace=True)

            school_groups.append(group_df)

            summary_df = summarize_group(group_df, cfg)
            school_group_summaries.append(summary_df)

            # get the top isp for the remaining schools
            top_isp = df.iloc[0]['isp']

            # at this point all remaining schools are ineligible for CEP
    # pass them along as a group of their own
    cum_isp = np.around((df['total_eligible'].cumsum() / df['total_enrolled'].cumsum()).astype(np.double) * 100, 2)
    df = df.assign(cum_isp=cum_isp)
    school_groups.append(df)

    summary_df = summarize_group(df, cfg)
    school_group_summaries.append(summary_df)

    return school_groups, school_group_summaries


#
# Function that implements a strategy to group schools with ISPs higher than (or equal to)
# that needed for 100% CEP funding.
#
def group_schools_hi_isp(df, cfg):
    school_groups = []
    school_group_summaries = []

    # group the data by cumulative ISP such that all schools with
    # max CEP threshold and higher are part of a single group; the
    # rest of the schools are in a second group

    bins = [0., cfg.max_cep_thold_pct() * 100, 100.]

    groups = df.groupby(pd.cut(df['cum_isp'], bins))
    ivals = groups.size().index.tolist()

    group_df = groups.get_group(ivals[-1]).apply(list).apply(pd.Series)
    summary_df = summarize_group(group_df, cfg)

    df.drop(group_df.index.tolist(), axis=0, inplace=True)
    # from among remaining schools see if any qualify based on isp impact
    schools_to_add = select_by_isp_impact(df, summary_df, (cfg.max_cep_thold_pct() * 100))

    if schools_to_add.shape[0] > 0:
        group_df = pd.concat([group_df, schools_to_add], axis=0)
        df.drop(schools_to_add.index.tolist(), axis=0, inplace=True)

    school_groups.append(group_df)

    summary_df = summarize_group(group_df, cfg)
    school_group_summaries.append(summary_df)

    return school_groups, school_group_summaries


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
def prepare_results_json(groups, summaries, cfg, metadata, ts, target_isp_width=None):
    json_result = {}

    # use default ISP width if not specified as  input
    isp_width = cfg.isp_width() if target_isp_width is None else target_isp_width

    n = len(groups)

    json_result['lea'] = metadata['lea']
    json_result['academic_year'] = metadata['academic_year']
    json_result['timestamp'] = ts

    groups_dl = []
    for i in range(n):
        g = summaries[i]

        eligibility = 'yes' if g.loc['sum', 'grp_isp'] >= (cfg.min_cep_thold_pct() * 100) else 'no'
        schools = groups[i].loc[:, 'school_code'].values.tolist()

        # json does not serialize numpy types. convert them to native ones below

        g_json = {"group": i,
                  "eligible_for_cep": eligibility,
                  "total_enrolled": int(g.loc['sum', 'total_enrolled']),
                  "direct_cert": int(g.loc['sum', 'direct_cert']),
                  "non_direct_cert": int(g.loc['sum', 'non_direct_cert']),
                  "total_eligible": int(g.loc['sum', 'total_eligible']),
                  "group_isp": round(float(g.loc['sum', 'grp_isp']), 2),
                  "group_size": int(g.loc['sum', 'size']),
                  "schools": schools}

        groups_dl.append(g_json)

    json_result['school_groups'] = {"num_groups": n, "group_summaries": groups_dl}
    json_result['mealscount_config_version'] = cfg.version()
    json_result['model_params'] = {'model_variant': cfg.model_variant(), 'isp_width': isp_width}

    # print(json_result)

    return json_result


#
# Function to return school group and summary data as html string
#
def prepare_results_html(groups, summaries, cfg, metadata, ts, target_isp_width=None):
    html_result = ""

    # use default ISP width if not specified as  input
    isp_width = cfg.isp_width() if target_isp_width is None else target_isp_width

    n = len(groups)

    html_result += """<table border="1">"""
    html_result += "<tr><td><b>LEA</b>: {}</td>".format(metadata['lea'])
    html_result += "<td><b>Academic Year</b>: {}</td>".format(metadata['academic_year'])

    html_result += "<td><b>Timestamp</b>: {}</td></tr>".format(ts)
    html_result += "</table>"

    # html_result += "<br>"
    # html_result += """<table border="1">"""
    # html_result += "<tr><td><b>Num Groups</b>: {}</td><tr>".format(n)
    # html_result += "</table>"
    # html_result += "<br>"

    html_result += """<table border="1">"""
    html_result += "<tr><th>Group</th><th>CEP Eligibility</th><th>Total Enrolled</th><th>Direct Certified</th>"
    html_result += "<th>Non-Direct Certified</th><th>Total Eligible</th><th>Group ISP</th><th>Group Size</th>"
    html_result += "<th>Schools</th>"

    groups_dl = []
    for i in range(n):
        g = summaries[i]

        eligibility = 'yes' if g.loc['sum', 'grp_isp'] >= (cfg.min_cep_thold_pct() * 100) else 'no'
        schools = groups[i].loc[:, 'school_code'].values.tolist()

        html_result += "<tr><td>{}</td><td>{}</td><td>{}</td>".format(i, eligibility,
                                                                      int(g.loc['sum', 'total_enrolled']))
        html_result += "<td>{}</td><td>{}</td><td>{}</td>".format(int(g.loc['sum', 'direct_cert']),
                                                                  int(g.loc['sum', 'non_direct_cert']),
                                                                  int(g.loc['sum', 'total_eligible']))
        html_result += "<td>{}</td><td>{}</td><td>{}</td>".format(round(float(g.loc['sum', 'grp_isp']), 2),
                                                                  int(g.loc['sum', 'size']),
                                                                  ", ".join([str(s) for s in schools]))
        html_result += "</tr>"

    html_result += "</table>"
    # html_result += "<br>"

    html_result += """<table border="1">"""
    html_result += "<tr><td><b>MealsCount Config Version</b>: {}</td>".format(cfg.version())
    html_result += "<td><b>Model Variant</b>: {}</td><td><b>ISP Width</b>: {}</td></tr>".format(cfg.model_variant(),
                                                                                                isp_width)
    html_result += "</table>"

    # print(html_result)

    return html_result


#
# Function to implement variant V2 of the algorithm
#
def runAlgorithmV2(self, data, cfg, bundle_groups=False):
    status = True

    md = data.metadata()
    df = data.to_frame()

    df = prepare_data(df)

    g1, s1 = group_schools_hi_isp(df, cfg)

    results_ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    if not bundle_groups:
        g2, s2 = group_schools_lo_isp(df, cfg)
        self.json_results = prepare_results_json(g1 + g2, s1 + s2, cfg, md, results_ts)
        self.html_results = prepare_results_html(g1 + g2, s1 + s2, cfg, md, results_ts)
    else:
        isp_width_bundle = cfg.isp_width_bundle()

        json_list = []
        html_list = []
        for isp_width in isp_width_bundle:
            g, s = group_schools_lo_isp(df.copy(), cfg, isp_width)
            json_list.append(prepare_results_json(g1 + g, s1 + s, cfg, md, results_ts, isp_width))
            html_list.append(prepare_results_html(g1 + g, s1 + s, cfg, md, results_ts, isp_width))

        self.json_results = {"bundles": json_list}
        self.html_results = "<br><br>".join(html_list)

        # uncomment below for debugging
    # show_results(g1+g2,s1+s2)

    return status


class mcAlgorithmV2(mcAlgorithm):
    """
    Implementation of the MealsCount Algorithm variant V2
    """

    def __init__(self):
        self.json_results = {}
        self.html_results = ""

    def version(self):
        return "v2"

    def run(self, data, cfg, bundle_groups=False):
        status = self.__run(data, cfg, bundle_groups)
        return status

    def get_school_groups(self, data, format="json"):
        if format == "json":
            return self.json_results
        elif format == "html":
            return self.html_results
        else:
            return data

    __run = runAlgorithmV2


#
# MAIN
#
def main():
    CWD = os.getcwd()

    DATADIR = "data"
    DATAFILE = "calpads_sample_data.xlsx"

    CONFIG_FILE = "config.json"

    data = bu.mcXLSchoolDistInput(os.path.join(DATADIR, DATAFILE))
    cfg = cp.mcModelConfig(CONFIG_FILE)

    strategy = mcAlgorithmV2() if cfg.model_variant() == "v2" else None

    grouper = CEPSchoolGroupGenerator(cfg, strategy)

    dataframe_groups = grouper.get_groups(data, 'df')
    json_bundles = grouper.get_group_bundles(data, 'df')

    json_groups = grouper.get_groups(data, "json")
    json_bundles = grouper.get_group_bundles(data, "json")

    html_groups = grouper.get_groups(data, "html")
    html_bundles = grouper.get_group_bundles(data, "html")

    # print(json.dumps(json_groups, indent=2))
    # print(json.dumps(json_bundles, indent=2))

    # print("<html><body>{}</body></html>".format(html_groups))
    print("<html><body>{}</body></html>".format(html_bundles))


# end: main

if __name__ == "__main__":
    main()
else:
    # do nothing
    pass

#
#
#
# import numpy as np
# import pandas as pd
# from bokeh.embed import components
# from bokeh.models import (
#     ColumnDataSource,
#     HoverTool
# )
# from bokeh.models import OpenURL
# from bokeh.models.tools import TapTool
# from bokeh.plotting import figure
# from .national_rates_config_parser import MCModelConfig
# import itertools as it
#
# config = MCModelConfig('config/national_config.json')
#
#
# # def brute_force(data, indexes_to_try):
# #     """this is the workhorse that does refining in the refined_100_percent() function
# #     it takes a list of indexes to try and all possibilities of combinations
# #     """
# #
# #     rv = []
# #     for i in range(7):
# #         for itry in it.combinations(indexes_to_try, i):
# #             data2 = data.iloc[list(set([*itry, *indexes_to_try]))]
# #             data2 = isp_sort(data2)
# #             data2 = data2.cumsum()
# #             data2.isp_percent = data2.isp_students / data2.total_enrollment
# #             if data2.isp_percent.tail(1).values > config.max_cep_thold_pct():
# #                 rv.append(data2.indexes.values)
# #     return rv
#
#
# # def best_of(data, indexes_to_try):
# #     """this just returns the best option from brute_force"""
# #     try_em = brute_force(data, indexes_to_try)
# #     values = [data.loc[x].total_enrollment.sum() for x in try_em]
# #     return try_em[max(range(len(values)), key=values.__getitem__)]
#
#
# def isp_sort(data):
#     """sort the elements by ISP percentage"""
#     data['isp_percent'] = data.isp_students / data.total_enrollment
#     data.sort_values(by=['isp_percent'], inplace=True, ascending=False)
#     return data
#
#
# # def get_isp_cumsum_greater_than(data, than_what=.40):
# #     """gives an index list of values where ISP_percent is > than_what"""
# #     data = isp_sort(data)
# #     data2 = data[["total_enrollment", "isp_students"]].cumsum()
# #     data2['isp_percent'] = data2.isp_students / data2.total_enrollment
# #     return data2[data2.isp_percent > than_what].index
# #
# #
# # def rough_100_percent_group(data, maximum_percentage_value=0):
# #     """
# #     this makes a rough group able to make the fully federal funded percent group = 100%
# #     I need to make a group of high ISP schools to start with
# #     """
# #     data = isp_sort(data)
# #     # data['ind'] = data.index.astype(str) + ','
# #     # data['index_cumsum'] = data['ind'].cumsum().str[:-1].str.split(',')
# #     # data.index_cumsum = data['index_cumsum'].apply(lambda x: list(map(int, x)))
# #     # data.set_index(data.index_cumsum)
# #
# #     # data2 is a temporary table to get the sum of the >62.5 percent schools
# #     data2 = data.cumsum()
# #     data2['isp_percent'] = data2.isp_students / data2.total_enrollment
# #     return data2[data2.isp_percent > maximum_percentage_value].index
#
#
# # def refined_100_percent(data, maximum_percentage_value=0):
# #     """
# #     this refines the group with a couple of tries.
# #     for large districts with more than 15 schools in the low ISP groups it may take a while
# #     """
# #     rough_100_percent_indexes = rough_100_percent_group(data, maximum_percentage_value=maximum_percentage_value)
# #     #    indexes_to_try = set(range(len(data))) - set(rough_100_percent_indexes)
# #     #    return best_of(data, indexes_to_try)
# #     return rough_100_percent_indexes
#
#
# # def divide_district_into_groups(data, excluded=[]):
# #     """
# #     we needed to divide the group into several schools of
# #     similar need to better categorize which ones we mix and match
# #     This is based on a k-means cluster of variable size depending on district size.
# #     """
# #     the_rest = set(data.indexes.values) - set(excluded)
# #     data['idx'] = data.index.values
# #     data['isp_percent'] = data.isp_students / data.total_enrollment
# #     the_rest = set(data.index.values) - set([1, 2])
# #     km = KMeans(n_clusters=len(data) // 10 + 2, random_state=0).fit(data[['idx', 'isp_percent']])
# #     data['cluster'] = km.labels_
#
#
# # def refined_minimum_percent_indexes(data, indexes_not_available):
# #     # todo currently the minumum is rough ... refine this
# #
# #     # data.reset_index()
# #     # data.drop('index_cumsum', axis=1)
# #     # data.set_index(['school_name', 'group'], inplace=True)
# #     data2 = data.copy()
# #     data2 = data2[data2['group'].isnull()]
# #     data2 = data2[['total_enrollment', 'isp_students', 'monthly_lunches_served', 'monthly_breakfast_served']].cumsum()
# #
# #     data2['isp_percent'] = data2.isp_students / data2.total_enrollment
# #
# #     rv1 = list(data2[data2.isp_percent > config.min_cep_thold_pct()].index)
# #     rv2 = data2.isp_percent[data2.isp_percent > config.min_cep_thold_pct()].tail(1).values
# #     return rv1, rv2
#
#
# # See mealcountsschool.py for a definition of objects in the mealCountsSchoolsArray
# def processSchools(data, **kwargs):  # state='CA', district="My District_Name"
#     """
#     Makes 2 groups of a district.
#     One is the group getting 100% funding
#     the other is a group that is above the minimum.
#     outputs 2 sections:
#     a data section in javascript
#     and a html section to render the data in.
#
#     e.g. data looks like this
#     data = pd.DataFrame(
#         {
#         "schoolnames":[str(x) for x in range(1000)],
#         "isp_students":[round(x*2.5) for x in range(1000)],
#         "total_enrollment": 3000,
#     })
#
#     config = pd.Series()
#     config.max_cep_thold_pct = .625
#     config.min_cep_thold_pct = .4
#
#     """
#
#     rates = config.cep_rates(region=kwargs['state'])
#     data['group'] = np.NaN
#
#     # gives an index list of values where ISP_percent is > .625 and defines that as "Group 1"
#     data = isp_sort(data)
#     top_group = data[["total_enrollment", "isp_students"]].cumsum()
#     top_group['isp_percent'] = top_group.isp_students / top_group.total_enrollment
#     one_hundred_percent_funding_indexes = top_group[top_group.isp_percent >= config.max_cep_thold_pct()].index
#     data.at[one_hundred_percent_funding_indexes, 'group'] = "Group 1"
#
#
#     # mask that to get the rest and find which of those isp_percent is > .4 and define that as "Group 2"
#
#     less_than_maximum = data[top_group.isp_percent < config.max_cep_thold_pct()]
#     #less_than_maximum_indexes = data[top_group.isp_percent < config.max_cep_thold_pct()].index
#     assert set(less_than_maximum.index).intersection(
#         set(one_hundred_percent_funding_indexes)) == set(), "still a problem: {}".format(
#         set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes)))
#
#     less_than_maximum = data.mask(top_group.isp_percent > config.max_cep_thold_pct())
#     mask_cumsum = less_than_maximum[["total_enrollment", "isp_students"]].cumsum()
#     mask_cumsum['isp_percent'] = mask_cumsum.isp_students / mask_cumsum.total_enrollment
#     min_percent_schools = less_than_maximum[mask_cumsum.isp_percent > config.min_cep_thold_pct()].index
#     data.at[min_percent_schools, 'group'] = "Group 2"
#     group_2_percent = mask_cumsum['isp_percent'][mask_cumsum.isp_percent > config.min_cep_thold_pct()].tail(1)
#
#     data['govt_funding_level'] = np.where(data.isp_percent * 1.6 > 1, 1, data.isp_percent * 1.6)
#     data.sort_values(['isp_percent', 'isp_students'],
#                      ascending=[False, False],
#                      inplace=True)
#     assert set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes)) == set(), \
#         "the 2 groups intersect: {}".format(data.iloc[set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes))].to_html())
#
#     # assistance = 0.06 * (True|False)
#     assistance = config.performance_based_cash_assistance_per_lunch() * kwargs['assistance']
#
#     data['federal_money_per_student_per_day'] = \
#         data.govt_funding_level * (rates.nslp_lunch_free_rate + assistance) + \
#         (1 - data.govt_funding_level) * (rates.nslp_lunch_paid_rate + assistance) + \
#         data.govt_funding_level * rates.sbp_bkfst_free_rate + \
#         (1 - data.govt_funding_level) * rates.sbp_bkfst_paid_rate
#     data['federal_money_per_month'] = data['federal_money_per_student_per_day'] * data.total_enrollment * \
#                                       config.monthly_lunches() * data.govt_funding_level
#
#     # target_area = data[[
#     #     'isp_students',
#     #     'total_enrollment',
#     #     'federal_money',
#     #     'monthly_lunches_served',
#     #     'monthly_breakfast_served']].cumsum()
#     # target_area['indexes'] = target_area.index.astype(str)
#     #
#     # target_area['isp_percent'] = target_area.isp_students / target_area.total_enrollment
#     # target_area['federal_funding_level'] = np.where(target_area.isp_percent * 1.6 >= 1, 1,
#     #                                                 target_area.isp_percent * 1.6)
#     #
#     # target_area.isp_percent = np.where(target_area.isp_percent>62.5, 62.5, target_area.isp_percent)
#
#     # format columns for plot
#     # target_area.total_enrollment = pd.to_numeric(target_area.total_enrollment)
#     # target_area.total_enrollment = target_area.total_enrollment.astype(np.int)
#     # target_area.drop(target_area[target_area.isp_percent > config.max_cep_thold_pct()].index, inplace=True)
#     # target_area = pd.concat([target_area, data.iloc[one_hundred_percent_funding_indexes]])
#
#     # p = figure(title="Monthly_Federal_Funding to Number_of_students Ratio",
#     #            plot_width=600,
#     #            plot_height=400,
#     #            tools=["pan", "tap", 'reset', 'zoom_in', 'wheel_zoom'])
#     #
#     # p.xaxis.axis_label = 'Number_of_students'
#     # p.yaxis.axis_label = 'Funding Percentage'
#     #
#     # # button from https://github.com/bokeh/bokeh/blob/master/examples/app/export_csv/main.py
#     # # button = Button(label="Download", button_type="success")
#     # # button.callback = CustomJS(args=dict(source=source),
#     # #                           code=open(join(dirname(__file__), "download.js")).read())
#     #
#     # source = ColumnDataSource(
#     #     data=dict(
#     #         x=target_area.total_enrollment,
#     #         y=target_area.federal_funding_level,
#     #         money=target_area.federal_money.apply(lambda x: '{:,.2f}'.format(x)),
#     #     )
#     # )
#     #
#     # # from the texas map
#     # p.circle(
#     #     x='x',
#     #     y='y',
#     #     source=source,
#     #     size=20,
#     #     fill_alpha=0.40,
#     #     hover_alpha=0.2,
#     #     line_color=None
#     #
#     # )
#     #
#     # p.add_tools(HoverTool(
#     #     tooltips=[
#     #         ("Funding Percent", "@y%"),
#     #         ("Student Population", "@x"),
#     #         ("Monthly Federal Funds", "$@money"),
#     #     ],
#     #     point_policy="snap_to_data"))
#     # # from https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html
#     # # # use the "color" column of the CDS to complete the URL
#     # # # e.g. if the glyph at index 10 is selected, then @color
#     # # # will be replaced with source.data['color'][10]
#     # url = "http://www.colors.commutercreative.com/"
#     # taptool = p.select(type=TapTool)
#     # taptool.callback = OpenURL(url=url)
#
#     data.set_index(['group', 'govt_funding_level'], inplace=True)
#     data = data[['isp_students', 'school_name', 'total_enrollment', 'isp_percent', 'federal_money_per_student_per_day',
#                  'federal_money_per_month']]
#     return data.to_html(), top_group.to_html(), mask_cumsum.to_html()
