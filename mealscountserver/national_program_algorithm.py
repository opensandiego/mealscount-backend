import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import (
    ColumnDataSource,
    HoverTool
)
from bokeh.models import OpenURL
from bokeh.models.tools import TapTool
from bokeh.plotting import figure
from .national_rates_config_parser import MCModelConfig
import itertools as it

config = MCModelConfig('config/national_config.json')


# def brute_force(data, indexes_to_try):
#     """this is the workhorse that does refining in the refined_100_percent() function
#     it takes a list of indexes to try and all possibilities of combinations
#     """
#
#     rv = []
#     for i in range(7):
#         for itry in it.combinations(indexes_to_try, i):
#             data2 = data.iloc[list(set([*itry, *indexes_to_try]))]
#             data2 = isp_sort(data2)
#             data2 = data2.cumsum()
#             data2.isp_percent = data2.isp_students / data2.total_enrollment
#             if data2.isp_percent.tail(1).values > config.max_cep_thold_pct():
#                 rv.append(data2.indexes.values)
#     return rv


# def best_of(data, indexes_to_try):
#     """this just returns the best option from brute_force"""
#     try_em = brute_force(data, indexes_to_try)
#     values = [data.loc[x].total_enrollment.sum() for x in try_em]
#     return try_em[max(range(len(values)), key=values.__getitem__)]


def isp_sort(data):
    """sort the elements by ISP percentage"""
    data['isp_percent'] = data.isp_students / data.total_enrollment
    data.sort_values(by=['isp_percent'], inplace=True, ascending=False)
    return data


# def get_isp_cumsum_greater_than(data, than_what=.40):
#     """gives an index list of values where ISP_percent is > than_what"""
#     data = isp_sort(data)
#     data2 = data[["total_enrollment", "isp_students"]].cumsum()
#     data2['isp_percent'] = data2.isp_students / data2.total_enrollment
#     return data2[data2.isp_percent > than_what].index
#
#
# def rough_100_percent_group(data, maximum_percentage_value=0):
#     """
#     this makes a rough group able to make the fully federal funded percent group = 100%
#     I need to make a group of high ISP schools to start with
#     """
#     data = isp_sort(data)
#     # data['ind'] = data.index.astype(str) + ','
#     # data['index_cumsum'] = data['ind'].cumsum().str[:-1].str.split(',')
#     # data.index_cumsum = data['index_cumsum'].apply(lambda x: list(map(int, x)))
#     # data.set_index(data.index_cumsum)
#
#     # data2 is a temporary table to get the sum of the >62.5 percent schools
#     data2 = data.cumsum()
#     data2['isp_percent'] = data2.isp_students / data2.total_enrollment
#     return data2[data2.isp_percent > maximum_percentage_value].index


# def refined_100_percent(data, maximum_percentage_value=0):
#     """
#     this refines the group with a couple of tries.
#     for large districts with more than 15 schools in the low ISP groups it may take a while
#     """
#     rough_100_percent_indexes = rough_100_percent_group(data, maximum_percentage_value=maximum_percentage_value)
#     #    indexes_to_try = set(range(len(data))) - set(rough_100_percent_indexes)
#     #    return best_of(data, indexes_to_try)
#     return rough_100_percent_indexes


# def divide_district_into_groups(data, excluded=[]):
#     """
#     we needed to divide the group into several schools of
#     similar need to better categorize which ones we mix and match
#     This is based on a k-means cluster of variable size depending on district size.
#     """
#     the_rest = set(data.indexes.values) - set(excluded)
#     data['idx'] = data.index.values
#     data['isp_percent'] = data.isp_students / data.total_enrollment
#     the_rest = set(data.index.values) - set([1, 2])
#     km = KMeans(n_clusters=len(data) // 10 + 2, random_state=0).fit(data[['idx', 'isp_percent']])
#     data['cluster'] = km.labels_


# def refined_minimum_percent_indexes(data, indexes_not_available):
#     # todo currently the minumum is rough ... refine this
#
#     # data.reset_index()
#     # data.drop('index_cumsum', axis=1)
#     # data.set_index(['school_name', 'group'], inplace=True)
#     data2 = data.copy()
#     data2 = data2[data2['group'].isnull()]
#     data2 = data2[['total_enrollment', 'isp_students', 'monthly_lunches_served', 'monthly_breakfast_served']].cumsum()
#
#     data2['isp_percent'] = data2.isp_students / data2.total_enrollment
#
#     rv1 = list(data2[data2.isp_percent > config.min_cep_thold_pct()].index)
#     rv2 = data2.isp_percent[data2.isp_percent > config.min_cep_thold_pct()].tail(1).values
#     return rv1, rv2


# See mealcountsschool.py for a definition of objects in the mealCountsSchoolsArray
def processSchools(data, **kwargs):  # state='CA', district="My District_Name"
    """
    Makes 2 groups of a district.
    One is the group getting 100% funding
    the other is a group that is above the minimum.
    outputs 2 sections:
    a data section in javascript
    and a html section to render the data in."""

    rates = config.cep_rates(region=kwargs['state'])
    data['group'] = np.NaN

    # gives an index list of values where ISP_percent is > .625 and defines that as "Group 1"
    data = isp_sort(data)
    top_group = data[["total_enrollment", "isp_students"]].cumsum()
    top_group['isp_percent'] = top_group.isp_students / top_group.total_enrollment
    one_hundred_percent_funding_indexes = top_group[top_group.isp_percent >= config.max_cep_thold_pct()].index
    data.at[one_hundred_percent_funding_indexes, 'group'] = "Group 1"


    # get the rest and find which of those isp_percent is > .4 and define that as "Group 2"

    less_than_maximum = data[top_group.isp_percent < config.max_cep_thold_pct()]
    #less_than_maximum_indexes = data[top_group.isp_percent < config.max_cep_thold_pct()].index
    assert set(less_than_maximum.index).intersection(
        set(one_hundred_percent_funding_indexes)) == set(), "still a problem: {}".format(
        set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes)))
    less_than_maximum = data.mask(top_group.isp_percent > config.max_cep_thold_pct())
    mask_cumsum = less_than_maximum[["total_enrollment", "isp_students"]].cumsum()
    mask_cumsum['isp_percent'] = mask_cumsum.isp_students / mask_cumsum.total_enrollment
    min_percent_schools = less_than_maximum[mask_cumsum.isp_percent > config.min_cep_thold_pct()].index
    data.at[min_percent_schools, 'group'] = "Group 2"
    group_2_percent = mask_cumsum['isp_percent'][mask_cumsum.isp_percent > config.min_cep_thold_pct()].tail(1)

    data['govt_funding_level'] = np.where(data.isp_percent * 1.6 > 1, 1, data.isp_percent * 1.6)
    data.sort_values(['isp_percent', 'isp_students'],
                     ascending=[False, False],
                     inplace=True)
    assert set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes)) == set(), \
        "the 2 groups intersect: {}".format(data.iloc[set(less_than_maximum.index).intersection(set(one_hundred_percent_funding_indexes))].to_html())

    # assistance = 0.06 * (True|False)
    assistance = config.performance_based_cash_assistance_per_lunch() * kwargs['assistance']

    data['federal_money_per_student_per_day'] = \
        data.govt_funding_level * (rates.nslp_lunch_free_rate + assistance) + \
        (1 - data.govt_funding_level) * (rates.nslp_lunch_paid_rate + assistance) + \
        data.govt_funding_level * rates.sbp_bkfst_free_rate + \
        (1 - data.govt_funding_level) * rates.sbp_bkfst_paid_rate
    data['federal_money_per_month'] = data['federal_money_per_student_per_day'] * data.total_enrollment * \
                                      config.monthly_lunches() * data.govt_funding_level

    # target_area = data[[
    #     'isp_students',
    #     'total_enrollment',
    #     'federal_money',
    #     'monthly_lunches_served',
    #     'monthly_breakfast_served']].cumsum()
    # target_area['indexes'] = target_area.index.astype(str)
    #
    # target_area['isp_percent'] = target_area.isp_students / target_area.total_enrollment
    # target_area['federal_funding_level'] = np.where(target_area.isp_percent * 1.6 >= 1, 1,
    #                                                 target_area.isp_percent * 1.6)
    #
    # target_area.isp_percent = np.where(target_area.isp_percent>62.5, 62.5, target_area.isp_percent)

    # format columns for plot
    # target_area.total_enrollment = pd.to_numeric(target_area.total_enrollment)
    # target_area.total_enrollment = target_area.total_enrollment.astype(np.int)
    # target_area.drop(target_area[target_area.isp_percent > config.max_cep_thold_pct()].index, inplace=True)
    # target_area = pd.concat([target_area, data.iloc[one_hundred_percent_funding_indexes]])

    # p = figure(title="Monthly_Federal_Funding to Number_of_students Ratio",
    #            plot_width=600,
    #            plot_height=400,
    #            tools=["pan", "tap", 'reset', 'zoom_in', 'wheel_zoom'])
    #
    # p.xaxis.axis_label = 'Number_of_students'
    # p.yaxis.axis_label = 'Funding Percentage'
    #
    # # button from https://github.com/bokeh/bokeh/blob/master/examples/app/export_csv/main.py
    # # button = Button(label="Download", button_type="success")
    # # button.callback = CustomJS(args=dict(source=source),
    # #                           code=open(join(dirname(__file__), "download.js")).read())
    #
    # source = ColumnDataSource(
    #     data=dict(
    #         x=target_area.total_enrollment,
    #         y=target_area.federal_funding_level,
    #         money=target_area.federal_money.apply(lambda x: '{:,.2f}'.format(x)),
    #     )
    # )
    #
    # # from the texas map
    # p.circle(
    #     x='x',
    #     y='y',
    #     source=source,
    #     size=20,
    #     fill_alpha=0.40,
    #     hover_alpha=0.2,
    #     line_color=None
    #
    # )
    #
    # p.add_tools(HoverTool(
    #     tooltips=[
    #         ("Funding Percent", "@y%"),
    #         ("Student Population", "@x"),
    #         ("Monthly Federal Funds", "$@money"),
    #     ],
    #     point_policy="snap_to_data"))
    # # from https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html
    # # # use the "color" column of the CDS to complete the URL
    # # # e.g. if the glyph at index 10 is selected, then @color
    # # # will be replaced with source.data['color'][10]
    # url = "http://www.colors.commutercreative.com/"
    # taptool = p.select(type=TapTool)
    # taptool.callback = OpenURL(url=url)

    data.set_index(['group', 'govt_funding_level'], inplace=True)
    data = data[['isp_students', 'school_name', 'total_enrollment', 'isp_percent', 'federal_money_per_student_per_day',
                 'federal_money_per_month']]
    return data.to_html(), top_group.to_html(), mask_cumsum.to_html()
