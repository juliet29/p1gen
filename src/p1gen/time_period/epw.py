from pathlib import Path
import polars as pl
from p1gen.config import WEATHER_FILE
from p1gen.time_period.epw_read import read_epw
import altair as alt
from p1gen.plot_utils.utils import AltairRenderers


# def read_epw(path: Path = WEATHER_FILE):
#     return EPW(path)

TEMPERATURE = "Dry Bulb Temperature"
WIND_SPEED = "Wind Speed"
WIND_DIRECTION = "Wind Direction"
qois = [TEMPERATURE, WIND_SPEED, WIND_DIRECTION]


def analyze_epw(path: Path = WEATHER_FILE):
    epw = read_epw(path)
    return epw


def prep_weather_plots():
    epw = analyze_epw().with_columns(
        month=pl.col.datetime.dt.month(), hour=pl.col.datetime.dt.hour()
    )
    data = (
        epw.group_by(pl.col.month, pl.col.hour, maintain_order=True)
        .agg(
            pl.col(TEMPERATURE).mean(),
            pl.col(WIND_SPEED).mean(),
            pl.col(WIND_DIRECTION).mean(),
        )
        .filter(pl.col.month.is_in(range(6, 11)))
    )

    row = alt.hconcat()

    for qoi in qois:
        tchart = data.plot.line(
            x="hour",
            y=alt.Y(f"{qoi}:Q").scale(zero=False),
            color=alt.Color("month:N").scale(scheme="viridis"),
        )
        row |= tchart

    row.show()


if __name__ == "__main__":
    AltairRenderers().set_renderer()
    prep_weather_plots()
    # day_ix = xr.date_range(start="2024-01-01",periods=24,  freq="h")
