from p1gen.plot_utils.utils import (
    convert_xarray_to_polars,
    group_dataset_by_time,
    AltairRenderers,
)
import xarray as xr
from typing import NamedTuple
import polars as pl
import altair as alt

from p1gen.time_period.data import (
    get_data_for_ach,
    get_data_for_flow,
    get_data_for_pressure,
    get_data_for_temperature_deviation,
    get_data_for_temperature_simple,
)
from typing import get_args, Literal, Protocol, Any
from p1gen.plot_utils.save import AltairChart


class TakesDFReturnsChart(Protocol):
    def __call__(self, df: pl.DataFrame, *args: Any, **kwds: Any) -> AltairChart: ...


TIME_OF_DAY = Literal["Day", "Night"]


class DayNightData(NamedTuple):
    day: xr.Dataset
    night: xr.Dataset

    def to_polars(self):
        def ds_to_polars(ds: xr.Dataset, time_of_day: TIME_OF_DAY):
            case_names = ["A", "B", "C"]
            df = (
                convert_xarray_to_polars(ds)
                .unpivot(on=case_names, index="datetimes")
                .drop_nulls()
            ).with_columns(time_of_day=pl.lit(time_of_day))
            return df

        dfs = [
            ds_to_polars(*i) for i in zip([self.day, self.night], get_args(TIME_OF_DAY))
        ]
        return pl.concat(dfs)


class QOIData(NamedTuple):
    max_diff_int_pressure: pl.DataFrame
    max_diff_ext_pressure: pl.DataFrame
    flow: pl.DataFrame
    temp: pl.DataFrame
    temp_dev: pl.DataFrame
    ach: pl.DataFrame

    def values(self):
        return self._asdict()


def get_day_night_data():
    max_diff_int_pressure, max_diff_ext_pressure = get_data_for_pressure()
    flow = get_data_for_flow()
    temp = get_data_for_temperature_simple()
    temp_dev = get_data_for_temperature_deviation()
    ach = get_data_for_ach()

    datas = [max_diff_int_pressure, max_diff_ext_pressure, flow, temp, temp_dev, ach]
    split_data = [DayNightData(*group_dataset_by_time(i)).to_polars() for i in datas]
    return QOIData(*split_data)


def plot_qoi_hist(df: pl.DataFrame, name: str):
    chart = (
        alt.Chart(df)
        .mark_bar(opacity=0.4, binSpacing=0)
        .encode(
            alt.X("value:Q").bin(maxbins=50).title(name),
            alt.Y("count()").stack(None),
            alt.Color("variable:N"),
            alt.Column("time_of_day:N"),
        )
    )
    return chart


def plot_qoi_box(df: pl.DataFrame, name: str):
    chart = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x=alt.X("variable").title(None).axis(labelAngle=0, labelFontSize=15),
            y=alt.Y("value").title(name).scale(zero=False),
            color=alt.Color("variable").scale(scheme="dark2").legend(None),
            column=alt.Column("time_of_day:N"),
        )
    )
    return chart


def make_group_plot(fx: TakesDFReturnsChart):
    data = get_day_night_data()
    row = alt.vconcat()
    for name, df in data.values().items():
        res = fx(df, name)
        row |= res
    return row


if __name__ == "__main__":
    AltairRenderers().set_renderer()

    boxplot = make_group_plot(plot_qoi_box)
    boxplot.show()

    histplot = make_group_plot(plot_qoi_hist)
    histplot.show()
