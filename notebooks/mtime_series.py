import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from p1gen.paths import  get_result_path, PATH_TO_IDD
    from p1gen.time_series import prep_case, prepare_heat_df, plot_by_zone, get_sample_chart, plot_exp_results, prepare_vol_df, prepare_temp_df
    from p1gen.qois import QOI, CalcQOI, Labels
    import xarray as xr
    import polars as pl
    return (
        PATH_TO_IDD,
        get_result_path,
        plot_exp_results,
        prep_case,
        prepare_temp_df,
        prepare_vol_df,
    )


@app.cell
def _(plot_exp_results):
    chart_heat = plot_exp_results()
    chart_heat.show()
    return


@app.cell
def _(plot_exp_results, prepare_vol_df):
    chart_vol = plot_exp_results(df_generating_fx=prepare_vol_df)
    chart_vol.show()
    return


@app.cell
def _(plot_exp_results, prepare_temp_df):
    chart_temp = plot_exp_results(df_generating_fx=prepare_temp_df)
    chart_temp.show()
    return


@app.cell
def _(PATH_TO_IDD, get_result_path, prep_case, prepare_temp_df):
    path = get_result_path(exp="case_amb_b1")
    case, sql = prep_case(PATH_TO_IDD, path)
    prepare_temp_df(case,sql)
    return case, sql


@app.cell
def _(case, prepare_vol_df, sql):
    prepare_vol_df(case, sql)
    return


if __name__ == "__main__":
    app.run()
