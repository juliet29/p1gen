from p1gen.qois import QOI, CalcQOI, DFC, Labels
from replan2eplus.results.sql import (
    create_result_for_qoi,
    get_sql_results,
    SQLiteResult,
)
from replan2eplus.ezcase.read import ExistCase
from p1gen.utils import convert_xarray_to_polars, filter_df_rooms, prep_case
import altair as alt
from p1gen.paths import EXP_NAMES, get_result_path, PATH_TO_IDD
from typing import get_args


def prepare_site_df(sql):
    site_temp = create_result_for_qoi(sql, QOI.SITE_TEMP).data_arr
    return convert_xarray_to_polars(site_temp, QOI.SITE_TEMP)


def prepare_temp_dev_df(sql):
    site_temp = create_result_for_qoi(sql, QOI.SITE_TEMP).data_arr
    plan_temp = create_result_for_qoi(sql, QOI.TEMP).data_arr
    diff = plan_temp - site_temp.squeeze()

    return convert_xarray_to_polars(diff, CalcQOI.ZONE_DEV_FROM_SITE_TEMP)


def plot_site(site_df):
    return (
        alt.Chart(site_df)
        .mark_line()
        .encode(
            x=alt.X(f"{DFC.DATETIMES}:T").title("Time").sort("ascending"),
            y=alt.Y(f"{QOI.SITE_TEMP}:Q").scale(zero=False).title(Labels.SITE_TEMP),
            color=alt.value("black"),
        )
    ).properties(width=400, height=100)


def plot_deviating(diff_df, title=""):
    return (
        alt.Chart(diff_df)
        .mark_line()
        .encode(
            x=alt.X(f"{DFC.DATETIMES}:T").title("Time").sort("ascending"),
            y=alt.Y(f"{CalcQOI.ZONE_DEV_FROM_SITE_TEMP}:Q").title(
                Labels.DEVIATION_FROM_SITE_TEMP
            ),
            color=alt.Color(f"{DFC.SPACE_NAMES}:N").title("Space Names"),
        )
    ).properties(width=200, height=100, title=title)


def plot_deviation_cases():
    # site_chart = plot_site(prepare_site_df(sql))
    def prepare_chart(exp: EXP_NAMES):
        path = get_result_path(exp)
        case, sql = prep_case(PATH_TO_IDD, path)
        diff_df = prepare_temp_dev_df(sql).pipe(filter_df_rooms)
        return plot_deviating(diff_df, case.folder_name)

    charts = [prepare_chart(e) for e in get_args(EXP_NAMES)]
    chart = (
        alt.hconcat(*charts).resolve_scale(color="independent", y="shared").resolve_axis(y="shared")
    )
    # .resolve_scale(y="shared").resolve_legend(color="independent")
    return chart
