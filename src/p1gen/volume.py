from typing import Literal
from p1gen.utils import read_idf
from p1gen.paths import test_case
from p1gen.geom_plot import create_geom_plot
from p1gen.read_sql import create_collections_for_variable, get_sql_results
from p1gen.data_helpers import create_dataframe_for_case
from p1gen.data_helpers import DFC
import altair as alt
import polars as pl


class QOI:
    # site
    WIND_SPEED = "Site Wind Speed"
    WIND_DIRECTION = "Site Wind Direction"
    SITE_TEMP = "Site Outdoor Air Drybulb Temperature,"

    # zone level
    TEMP = "Zone Mean Air Temperature"
    VENT_VOL = "AFN Zone Ventilation Volume"
    MIX_VOL = "AFN Zone Mixing Volume"
    NODE_PRESSURE = "AFN Node Total Pressure"

    MIX_HEAT_GAIN_RATE = "AFN Zone Mixing Sensible Heat Gain Rate"
    MIX_HEAT_LOSS_RATE = "AFN Zone Mixing Sensible Heat Loss Rate"

    VENT_HEAT_GAIN_RATE = "AFN Zone Ventilation Sensible Heat Gain Rate"
    VENT_HEAT_LOSS_RATE = "AFN Zone Ventilation Sensible Heat Loss Rate"

    # subsurface / surface
    FLOW_12 = "AFN Linkage Node 1 to Node 2 Volume Flow Rate"
    FLOW_21 = "AFN Linkage Node 2 to Node 1 Volume Flow Rate"

    # surface like..
    WIND_PRESSURE = ""  # TODO!


class CalcQOI:
    MIX_NET_HEAT_RATE = "AFN Zone Mixing Net Heat Exchange Rate"  # MINE!
    VENT_NET_HEAT_RATE = "AFN Zone Ventilation Net Heat Exchange Rate"
    NET_FLOW = "AFN Linkage Net Volume Flow Rate"


def prep_case():
    case = read_idf(test_case)
    sql_results = get_sql_results(test_case)
    return case, sql_results


def print_spaces(df: pl.DataFrame):
    print(df[DFC.SPACE_NAMES].unique().to_list())


def prep_heat_df():
    case, sql = prep_case()
    heat_rate_df = (
        create_dataframe_for_case(
            sql,
            [
                QOI.MIX_HEAT_GAIN_RATE,
                QOI.MIX_HEAT_LOSS_RATE,
                QOI.VENT_HEAT_GAIN_RATE,
                QOI.VENT_HEAT_LOSS_RATE,
            ],
            case,
        )
        .with_columns(
            (pl.col(QOI.MIX_HEAT_GAIN_RATE) - pl.col(QOI.MIX_HEAT_LOSS_RATE)).alias(
                CalcQOI.MIX_NET_HEAT_RATE
            ),
            (pl.col(QOI.VENT_HEAT_GAIN_RATE) - pl.col(QOI.VENT_HEAT_LOSS_RATE)).alias(
                CalcQOI.VENT_NET_HEAT_RATE
            ),
        )
        .select(
            pl.exclude(
                [
                    QOI.MIX_HEAT_GAIN_RATE,
                    QOI.MIX_HEAT_LOSS_RATE,
                    QOI.VENT_HEAT_GAIN_RATE,
                    QOI.VENT_HEAT_LOSS_RATE,
                ]
            )
        )
        .unpivot(
            on=[CalcQOI.VENT_NET_HEAT_RATE, CalcQOI.MIX_NET_HEAT_RATE],
            index=[DFC.SPACE_NAMES, DFC.DATETIMES],
        )
    )
    print(heat_rate_df)
    return heat_rate_df


def prep_vol_df():
    case, sql = prep_case()
    vol_df = (
        create_dataframe_for_case(sql, [QOI.MIX_VOL, QOI.VENT_VOL], case)
        .unpivot(
            on=[QOI.MIX_VOL, QOI.VENT_VOL],
            index=[DFC.SPACE_NAMES, DFC.DATETIMES],
        )
        .fill_null("zero")
    )

    # collections = create_collections_for_variable(sql, QOI.MIX_VOL)

    # TODO can do the opposte -> set a flag
    # valid_collections = [i for i in collections if i.space_name in case.geom_names]

    # filter zones where all values are 0..
    print(vol_df)
    return vol_df


def plot_mix_volume_by_room():
    vol_df = prep_heat_df() #prep_vol_df()
    # TODO verify the schema
    chart = (
        alt.Chart(vol_df)
        .mark_line()
        .encode(
            x=f"{DFC.DATETIMES}:T",
            y=f"{DFC.VALUE}:Q",
            color=f"{DFC.SPACE_NAMES}:N",
            strokeDash=alt.StrokeDash(f"{DFC.VARIABLE}:N"),
        )
        .facet(column=f"{DFC.SPACE_NAMES}:N")
    )

    # .sort(order=[QOI.VENT_VOL, QOI.MIX_VOL]),
    # heat_chart = alt.Chart(vol_df).mark_line().encode(
    #     x=f'{DFC.DATETIMES}:T',
    #     y=f'{CalcQOI.MIX_NET_HET_RATE}:Q',
    #     color=f'{DFC.SPACE_NAMES}:N'
    # )

    # chart = alt.layer(mix_chart)

    chart.show()


if __name__ == "__main__":
    RendererTypes = Literal["browser", "html"]
    BROWSER = "browser"
    HTML = "html"
    alt.renderers.enable(BROWSER)
    # prep_vol_df()
    #prep_heat_df()
    plot_mix_volume_by_room()
    # case = read_idf(test_case)
    # sql_results = get_sql_results(test_case)
    # flow_df = create_dataframe_for_case(sql_results, [QOI.FLOW_12, QOI.FLOW_21], case)
    # # p = flow_df.to_pandas()
    # unique_spaces = flow_df[DFC.SPACE_NAMES].unique()
    # print(unique_spaces.to_list())
    # print(flow_df)
    # pass

    # print(vol_df)

    # pressure_df = create_dataframe_for_case(sql_results, [QOI.NODE_PRESSURE], case)
    # print(pressure_df)
    # create_geom_plot(case)


# if is exterior -> then goes to direction
# other wise goes to its nb..

# maybe the appending data shuld be an after thing??
# space name | zone name | neighbor: direction or zone
# where to put arrow depends on net differemce..
# addiing arrows to lines in mpl? + adjusting thickness.?
