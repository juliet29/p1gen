from typing import Literal
from p1gen.utils import read_idf
from p1gen.paths import test_case
from p1gen.geom_plot import create_geom_plot
from p1gen.read_sql import create_collections_for_variable, get_sql_results
from p1gen.data_helpers import create_dataframe_for_case
from p1gen.data_helpers import DFC
import altair as alt
import polars as pl
from pathlib import Path


class Labels:
    NET_HEAT_EXCHANGE = "AFN Zone Net Heat Exchange Rate [W]"
    MIXVENT_VOLUME = "AFN Zone Volume [m3]"  #  averaged over time step


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


def prep_case(path:Path):
    case = read_idf(path)
    sql_results = get_sql_results(path)
    return case, sql_results


def print_spaces(df: pl.DataFrame):
    print(df[DFC.SPACE_NAMES].unique().to_list())


def prep_heat_df(case, sql):
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
    return heat_rate_df


def prep_vol_df(case, sql):
    vol_df = (
        create_dataframe_for_case(sql, [QOI.MIX_VOL, QOI.VENT_VOL], case)
        .unpivot(
            on=[QOI.MIX_VOL, QOI.VENT_VOL],
            index=[DFC.SPACE_NAMES, DFC.DATETIMES],
        )
        .fill_null("zero")
    )
    return vol_df


def plot_by_zone(df: pl.DataFrame, ytitle: str):
    # TODO verify the schema
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(f"{DFC.DATETIMES}:T").title("Time").sort("ascending"),
            y=alt.Y(f"{DFC.VALUE}:Q").title(ytitle),
            color=f"{DFC.SPACE_NAMES}:N",
            strokeDash=alt.StrokeDash(f"{DFC.VARIABLE}:N"),
        )
        .facet(column=f"{DFC.SPACE_NAMES}:N")
    )

    chart.show()

    return chart


def make_plots_by_zone(path: Path):
    case, sql = prep_case(path)
    heat_df = prep_heat_df(case, sql)
    vol_df = prep_vol_df(case, sql)

    vol_chart = plot_by_zone(vol_df, Labels.MIXVENT_VOLUME).properties(title=path.name)

    heat_chart = plot_by_zone(heat_df, Labels.NET_HEAT_EXCHANGE).properties(
        title=path.name
    )

    return vol_chart, heat_chart


if __name__ == "__main__":
    RendererTypes = Literal["browser", "html"]
    BROWSER = "browser"
    HTML = "html"
    alt.renderers.enable(BROWSER)
    # prep_vol_df()
    # prep_heat_df()
