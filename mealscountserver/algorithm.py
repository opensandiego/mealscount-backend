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

minimum_percentage_value = .30  # 30% to receive funds
maximum_percentage_value = .625  # 62.5% where you get 100% federal funding

# figures come from SP15-2013a2v3.xls from the federal Govt.
# < website needed >
contenential_us = ['AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
                   'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
                   'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
state_rates = pd.DataFrame(
    [
        ('HI', 3.78, 0.36, 2.03, 0.34),
        ('AK', 5.24, 0.50, 2.79, 0.45),
        ('PR', 3.78, 0.36, 2.03, 0.34),
        *((state, 3.23, 0.31, 1.75, 0.30) for state in contenential_us)
    ],
    columns=["state_or_territory",
             "NSLP_lunch_free_rate",
             "NSLP_lunch_paid_rate",
             "SBP_breakfast_free_rate",
             "SBP_breakfast_paid_rate"
             ]
)


# See mealcountsschool.py for a definition of objects in the mealCountsSchoolsArray
def processSchools(data, **kwargs):  # state='CA', district="My District_Name"
    """outputs 2 sections:
    a data section in javascript
    and a html section to render the data in."""

    rates = state_rates[state_rates.state_or_territory == kwargs['state']]

    data['isp_percent'] = data.isp_students / data.total_enrollment
    data.sort_values(['isp_percent'], ascending=False, inplace=True)
    # data['above_indexes'] = data[data.isp_percent >= data.isp_percent].index.tolist()

    data['ind'] = data.index.astype(str) + ','
    data['index_cumsum'] = data['ind'].cumsum().str[:-1].str.split(',')
    data.index_cumsum = data['index_cumsum'].apply(lambda x: list(map(int, x)))

    # data2 is a temporary table to get the sum of the >62.5 percent schools
    data2 = data[['total_enrollment', 'isp_students', 'monthly_lunches_served', 'monthly_breakfast_served']].cumsum()
    data2['isp_percent'] = data2.isp_students / data2.total_enrollment

    one_hundred_percent_funding_indexes = data2[data2.isp_percent > maximum_percentage_value].index
    one_hundred_percent_funding = data2[data2.isp_percent > maximum_percentage_value].tail(1)
    one_hundred_percent_funding[
        'isp_percent'] = one_hundred_percent_funding.isp_students / one_hundred_percent_funding.total_enrollment
    # edited

    data['govt_funding_level'] = np.where(data.isp_percent * 1.6 > 1, 1, data.isp_percent * 1.6)
    data.sort_values(['isp_percent', 'isp_students'],
                     ascending=[False, False],
                     inplace=True)

    data['federal_money'] = \
        data.monthly_lunches_served * (data.govt_funding_level) * rates.NSLP_lunch_free_rate.iloc[0] + \
        data.monthly_lunches_served * (1 - data.govt_funding_level) * rates.NSLP_lunch_paid_rate.iloc[0] + \
        data.monthly_breakfast_served * data.govt_funding_level * rates.SBP_breakfast_free_rate.iloc[0] + \
        data.monthly_breakfast_served * (1 - data.govt_funding_level) * rates.SBP_breakfast_paid_rate.iloc[0]

    target_area = data[[
        'isp_students',
        'total_enrollment',
        'federal_money',
        'monthly_lunches_served',
        'monthly_breakfast_served']].cumsum()
    target_area['indexes'] = target_area.index.astype(str)

    target_area['isp_percent'] = target_area.isp_students / target_area.total_enrollment
    target_area['federal_funding_level'] = np.where(target_area.isp_percent * 1.6 >= 1, 1,
                                                    target_area.isp_percent * 1.6)

    # target_area.isp_percent = np.where(target_area.isp_percent>62.5, 62.5, target_area.isp_percent)

    # format columns for plot
    target_area.total_enrollment = pd.to_numeric(target_area.total_enrollment)
    target_area.total_enrollment = target_area.total_enrollment.astype(np.int)
    target_area.drop(target_area[target_area.isp_percent > maximum_percentage_value].index, inplace=True)
    target_area = pd.concat([target_area, one_hundred_percent_funding])

    p = figure(title="Monthly_Federal_Funding to Number_of_students Ratio",
               plot_width=600,
               plot_height=400,
               tools=["pan", "tap", 'reset', 'zoom_in', 'wheel_zoom'])

    p.xaxis.axis_label = 'Number_of_students'
    p.yaxis.axis_label = 'Funding Percentage'

    # button from https://github.com/bokeh/bokeh/blob/master/examples/app/export_csv/main.py
    # button = Button(label="Download", button_type="success")
    # button.callback = CustomJS(args=dict(source=source),
    #                           code=open(join(dirname(__file__), "download.js")).read())

    source = ColumnDataSource(
        data=dict(
            x=target_area.total_enrollment,
            y=target_area.federal_funding_level * 100,
            money=target_area.federal_money.apply(lambda x: '{:,.2f}'.format(x)),
        )
    )

    # from the texas map
    p.circle(
        x='x',
        y='y',
        source=source,
        size=20,
        fill_alpha=0.40,
        hover_alpha=0.2,
        line_color=None

    )

    p.add_tools(HoverTool(
        tooltips=[
            ("Funding Percent", "@y%"),
            ("Student Population", "@x"),
            ("Monthly Federal Funds", "$@money"),
        ],
        #    renderers=[cr],
        #    mode='hline',
        point_policy="snap_to_data"))
    # from https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/callbacks.html
    # # use the "color" column of the CDS to complete the URL
    # # e.g. if the glyph at index 10 is selected, then @color
    # # will be replaced with source.data['color'][10]
    url = "http://www.colors.commutercreative.com/"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    return components(p)
