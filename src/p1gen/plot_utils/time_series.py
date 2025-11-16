from typing import Callable, get_args

import altair as alt
import polars as pl
import xarray as xr
from replan2eplus.ezcase.ez import EZ
from replan2eplus.results.sql import (
    SQLiteResult,
    create_result_for_qoi,
)

from p1gen.paths import EXP_NAMES, ep_paths, get_result_path
from p1gen.plot_utils.labels import DFC, CalcQOI
from p1gen.plot_utils.qois import QOI
from p1gen.plot_utils.utils import convert_xarray_to_polars, filter_df_rooms, prep_case


def prepare_heat_df(case: ExistCase, sql: SQLiteResult):
    mix_heat_gain = create_result_for_qoi(sql, QOI.MIX_HEAT_GAIN_RATE)
    mix_heat_loss = create_result_for_qoi(sql, QOI.MIX_HEAT_LOSS_RATE)
    net_mix = mix_heat_gain - mix_heat_loss

    vent_heat_gain = create_result_for_qoi(sql, QOI.VENT_HEAT_GAIN_RATE)
    vent_heat_loss = create_result_for_qoi(sql, QOI.VENT_HEAT_LOSS_RATE)
    net_vent = vent_heat_gain - vent_heat_loss

    # TODO should set this when the data arr is created!
    net_mix.data_arr.name = CalcQOI.MIX_NET_HEAT_RATE
    net_vent.data_arr.name = CalcQOI.VENT_NET_HEAT_RATE

    res = xr.merge([net_mix.data_arr, net_vent.data_arr])

    df = convert_xarray_to_polars(res).unpivot(
        on=[CalcQOI.MIX_NET_HEAT_RATE, CalcQOI.VENT_NET_HEAT_RATE],
        index=[DFC.SPACE_NAMES, DFC.DATETIMES],
    )

    return df


def prepare_vol_df(case: ExistCase, sql: SQLiteResult):
    mix_vol = create_result_for_qoi(sql, QOI.MIX_VOL)
    vent_vol = create_result_for_qoi(sql, QOI.VENT_VOL)

    mix_vol.data_arr.name = QOI.MIX_VOL
    vent_vol.data_arr.name = QOI.VENT_VOL

    res = xr.merge([mix_vol.data_arr, vent_vol.data_arr])
    df = convert_xarray_to_polars(res).unpivot(
        on=[QOI.MIX_VOL, QOI.VENT_VOL],
        index=[DFC.SPACE_NAMES, DFC.DATETIMES],
    )
    return df


def prepare_temp_df(case: ExistCase, sql: SQLiteResult):
    temp = create_result_for_qoi(sql, QOI.TEMP)

    temp.data_arr.name = QOI.TEMP

    res = xr.merge([temp.data_arr])
    df = convert_xarray_to_polars(res).unpivot(
        on=[QOI.TEMP],
        index=[DFC.SPACE_NAMES, DFC.DATETIMES],
    )
    return df


def plot_by_zone(df: pl.DataFrame, ytitle: str, case_name: str = ""):
    # TODO verify the schema
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(f"{DFC.DATETIMES}:T").title("Time").sort("ascending"),
            y=alt.Y(f"{DFC.VALUE}:Q").title(ytitle),
            color=alt.Color(f"{DFC.VARIABLE}:N").title("Variable"),
            column=alt.Column(f"{DFC.SPACE_NAMES}:N").title(""),
        )
    ).properties(title=case_name, width=170, height=100)

    return chart


# TODO this all goes elsewhwere
# TODO separate the experiment unique stuff..

DFGeneratingFx = Callable[[ExistCase, SQLiteResult], pl.DataFrame]


def get_sample_chart(exp: EXP_NAMES, df_generating_fx: DFGeneratingFx, label: str):
    path = get_result_path(exp)
    case, sql = prep_case(ep_paths.idd_path, path)
    df = df_generating_fx(case, sql).pipe(filter_df_rooms)
    return plot_by_zone(df, label, case_name=exp)


def plot_exp_results(
    label: str,
    df_generating_fx: DFGeneratingFx = prepare_heat_df,
):
    charts = [get_sample_chart(i, df_generating_fx, label) for i in get_args(EXP_NAMES)]
    chart = (
        alt.vconcat(*charts)
        .resolve_scale(y="shared")
        .configure_legend(
            labelLimit=300,
            strokeColor="gray",
            padding=10,
            cornerRadius=10,
            orient="top",
        )
    )
    return chart


if __name__ == "__main__":
    plot_exp_results()
