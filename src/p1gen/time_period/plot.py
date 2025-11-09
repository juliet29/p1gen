from p1gen.paths import CampaignNameOptions
from p1gen.time_period.data import (
    get_data_for_ach,
    get_data_for_pressure,
    get_data_for_flow,
    get_data_for_temperature,
)
from p1gen.plot_utils.utils import convert_xarray_to_polars, AltairRenderers
import xarray as xr
import altair as alt

alt.renderers.enable(AltairRenderers.BROWSER)


def create_box_plot(campaign_name: CampaignNameOptions = "20251109_summer"):
    pressure_int, pressure_ext = get_data_for_pressure(campaign_name)
    print(pressure_int.mean())

    p_int_df = convert_xarray_to_polars(pressure_int)
    chart = alt.Chart(p_int_df).mark_boxplot().encode(x="A")
    return pressure_int


def make_boxplot(ds: xr.Dataset, name: str):
    # using the xarray validate is helpful here
    assert "datetimes" in ds.coords
    ds6h = ds.resample(datetimes="6h").median()
    df = convert_xarray_to_polars(ds6h)
    source = df.unpivot(index="datetimes", on=["A", "B", "C"])
    chart = (
        alt.Chart(source)
        .mark_boxplot()
        .encode(x="variable", y=alt.Y("value").title(name))
    )
    return chart


def get_data_and_make_plots(campaign_name: CampaignNameOptions = "20251109_summer"):
    internal_pressures_max_dif, ext_p = get_data_for_pressure(campaign_name)
    net_flow_plan_median = get_data_for_flow(campaign_name).median(dim="space_names")
    ach_plan_median = get_data_for_ach(campaign_name).median(dim="space_names")
    night_temp_dev_plan_median, day_temp_dev_plan_median = get_data_for_temperature(
        campaign_name
    )

    datasets = [
        internal_pressures_max_dif,
        net_flow_plan_median,
        ach_plan_median,
        night_temp_dev_plan_median,
    ]
    names = ["pressure", "flow", "ach", "night_temp"]

    row = alt.hconcat()
    for data, name in zip(datasets, names):
        chart = make_boxplot(data, name)
        row |= chart

    row.show()


if __name__ == "__main__":
    get_data_and_make_plots()
