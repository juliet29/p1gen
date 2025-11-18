from pathlib import Path
import polars as pl
from p1gen.config import (
    DEBUG_FIGURES,
    WEATHER_FILE,
    CURRENT_CAMPAIGN,
    STUDY_DATE,
    STUDY_HOUR,
)
from p1gen.time_period.epw_read import read_epw
import altair as alt
from p1gen.plot_utils.utils import AltairRenderers
from p1gen.plot_utils.save import save_figure
from datetime import datetime


# def read_epw(path: Path = WEATHER_FILE):
#     return EPW(path)

TEMPERATURE = "Dry Bulb Temperature"
WIND_SPEED = "Wind Speed"
WIND_DIRECTION = "Wind Direction"
qois = [TEMPERATURE, WIND_SPEED, WIND_DIRECTION]

units = ["[ºC]", "[m/s]", "[º]"]


def analyze_epw(path: Path = WEATHER_FILE):
    epw = read_epw(path)
    return epw


def conditions_at_geom_time(
    date_: tuple[int, int, int] = STUDY_DATE, hour: int = STUDY_HOUR
):
    datetime_ = datetime(*date_, hour)
    epw = analyze_epw()
    return epw.filter(pl.col.datetime == datetime_).select(
        ["Wind Direction", "Dry Bulb Temperature", "Wind Speed"]
    )


@save_figure(CURRENT_CAMPAIGN, "site_temp", DEBUG_FIGURES)
def prep_weather_plots():
    epw = analyze_epw().with_columns(
        month=pl.col.datetime.dt.month(),
        hour=pl.col.datetime.dt.hour(),
        month_string=pl.col.datetime.dt.strftime("%B"),
    )
    print(epw)
    data = (
        epw.group_by(pl.col.month, pl.col.hour, maintain_order=True)
        .agg(
            pl.col(TEMPERATURE).mean(),
            pl.col(WIND_SPEED).median(),
            pl.col(WIND_DIRECTION).median(),
            pl.col("month_string").first(),
        )  # TODO: line up with the analsis period
        .filter(pl.col.month.is_in(range(6, 11)))
    )

    print(data)

    row = alt.hconcat()

    for qoi, unit in zip(qois, units):
        name = f"{qoi} {unit}"
        tchart = data.plot.line(
            x=alt.X("hour").title("Hour of Day"),
            y=alt.Y(f"{qoi}:Q").scale(zero=False).title(name),
            color=alt.Color("month_string:O")
            .scale(scheme="viridis")
            .title("Months")
            .sort(),
        )
        row |= tchart

    # row.show()
    return row


if __name__ == "__main__":
    AltairRenderers().set_renderer()
    prep_weather_plots()
    # day_ix = xr.date_range(start="2024-01-01",periods=24,  freq="h")
