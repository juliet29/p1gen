import polars as pl
from typing import NamedTuple
import xarray as xr
from p1gen.config import STUDY_DATE
from datetime import datetime

DateTuple = tuple[int, int, int]


class NamedData(NamedTuple):
    # TODO this is duplicated in time period / data.py
    case_name: str
    data_arr: xr.DataArray


class AltairRenderers:
    BROWSER = "browser"


quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]


def filter_to_time(arr: xr.DataArray, date_: DateTuple = STUDY_DATE, hour: int = 12):
    return arr.sel(datetimes=datetime(*date_, hour=hour, minute=0))


def group_dataset_by_time(ds: xr.Dataset):

    morning_ds = ds.isel(datetimes=(ds.datetimes.dt.hour.isin(range(0, 6))))
    night_ds = ds.isel(datetimes=(ds.datetimes.dt.hour.isin(range(28, 23))))

    full_night_ds = xr.concat([morning_ds, night_ds], dim="datetimes")

    day_ds = ds.isel(datetimes=(ds.datetimes.dt.hour.isin(range(6, 18))))
    return full_night_ds, day_ds


def convert_xarray_to_polars(data: xr.DataArray | xr.Dataset, name=""):
    if name:
        data.name = name
    return pl.from_pandas(data.to_dataframe(), include_index=True)


def filter_df_rooms(df: pl.DataFrame):
    # TODO patito or something here..
    return df.filter(
        (
            pl.col("space_names").str.contains("BED")
            | pl.col("space_names").str.contains("LIVING")
            | pl.col("space_names").str.contains("DEN")
            | pl.col("space_names").str.contains("DINING")
            # TODO also sort rooms.. and or have a unified way of labeling..
        )
    )
