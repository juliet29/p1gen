import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from p1gen.paths import  get_result_path, PATH_TO_IDD
    from p1gen.time_series import prep_case, prepare_heat_df, plot_by_zone, get_sample_chart, plot_exp_results, prepare_vol_df, prepare_temp_df, filter_df_rooms
    from p1gen.qois import QOI, CalcQOI, Labels, DFC
    import xarray as xr
    import polars as pl
    from replan2eplus.results.sql import create_result_for_qoi
    import altair as alt
    from p1gen.utils import convert_xarray_to_polars
    from p1gen.deviation import plot_deviation_cases
    return (
        DFC,
        PATH_TO_IDD,
        QOI,
        alt,
        convert_xarray_to_polars,
        create_result_for_qoi,
        filter_df_rooms,
        get_result_path,
        plot_deviation_cases,
        prep_case,
        prepare_temp_df,
    )


@app.cell
def _(plot_deviation_cases):
    plot_deviation_cases()
    return


@app.cell
def _(PATH_TO_IDD, get_result_path, prep_case, prepare_temp_df):
    path = get_result_path(exp="case_b")
    case, sql = prep_case(PATH_TO_IDD, path)
    temp_df = prepare_temp_df(case,sql)
    return case, sql


@app.cell
def _(case, plot_case, sql):
    charts = plot_case(case, sql)
    charts
    return


@app.cell
def _(case):
    case.path_to_initial_idf.parts[-2]
    return


@app.cell
def _(QOI, create_result_for_qoi, sql):
    temp_arr = create_result_for_qoi(sql, QOI.TEMP).data_arr
    temp_arr
    return (temp_arr,)


@app.cell
def _(QOI, create_result_for_qoi, sql):
    site_temp_arr = create_result_for_qoi(sql, QOI.SITE_TEMP)
    site_temp_arr
    return (site_temp_arr,)


@app.cell
def _(site_temp_arr):
    site_temp_arr.data_arr.squeeze()
    return


@app.cell
def _(DFC, temp_arr):
    mean_temp = temp_arr.median(dim=DFC.SPACE_NAMES)
    MEAN_TEMP_NAME = "Mean Temp Across All Zones"
    mean_temp.name = MEAN_TEMP_NAME
    return MEAN_TEMP_NAME, mean_temp


@app.cell
def _(convert_xarray_to_polars, mean_temp):
    mean_temp_df = convert_xarray_to_polars(mean_temp)
    mean_temp_df
    return (mean_temp_df,)


@app.cell
def _(mean_temp, temp_arr):
    temp_diff  = temp_arr - mean_temp
    TEMP_DIFF = "Temp Difference"
    temp_diff.name = TEMP_DIFF
    temp_diff
    return TEMP_DIFF, temp_diff


@app.cell
def _(site_temp_arr, temp_arr):
    site_diff = temp_arr - site_temp_arr.data_arr.squeeze()
    site_diff
    return


@app.cell
def _(convert_xarray_to_polars, filter_df_rooms, temp_diff):
    diff_df = convert_xarray_to_polars(temp_diff).pipe(filter_df_rooms)
    diff_df
    return (diff_df,)


@app.cell
def _(DFC, TEMP_DIFF, alt, diff_df):
    ytitle="Difference from Median Temperature [ºC]"
    diff_chart = (
            alt.Chart(diff_df)
            .mark_line()
            .encode(
                x=alt.X(f"{DFC.DATETIMES}:T").title("Time").sort("ascending"),
                y=alt.Y(f"{TEMP_DIFF}:Q").title(ytitle),
                color=alt.Color(f"{DFC.SPACE_NAMES}:N").title("Space Names"),
            )
        )
    diff_chart.show()
    return (diff_chart,)


@app.cell
def _(DFC, MEAN_TEMP_NAME, alt, mean_temp_df):
    mean_chart = (
        alt.Chart(mean_temp_df).mark_line().encode(
                x=alt.X(f"{DFC.DATETIMES}:T").title("Time").sort("ascending"),
                y=alt.Y(f"{MEAN_TEMP_NAME}:Q").title("Median Temp Across Zones [ºC]").scale(zero=False),
            color=alt.value("black")
        )
    )
    mean_chart.show()
    return (mean_chart,)


@app.cell
def _(alt, diff_chart, mean_chart):
    alt.hconcat(mean_chart, diff_chart)
    return


if __name__ == "__main__":
    app.run()
