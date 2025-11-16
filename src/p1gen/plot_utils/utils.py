import polars as pl
from typing import NamedTuple
import xarray as xr
from p1gen.config import STUDY_DATE
from datetime import datetime

DateTuple = tuple[int, int, int]


def filter_to_time(arr: xr.DataArray, date_: DateTuple = STUDY_DATE, hour: int = 12):
    return arr.sel(datetimes=datetime(*date_, hour=hour, minute=0))


class AltairRenderers:
    BROWSER = "browser"


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


class NamedData(NamedTuple):
    # TODO this is duplicated in time period / data.py
    case_name: str
    data_arr: xr.DataArray


# def prep_case(
#     path_to_idd: Path,
#     path_to_case: Path,
# ):
#     case = ExistCase(path_to_idd, path_to_case / "out.idf")
#     sql_results = get_sql_results(path_to_case)
#     return case, sql_results
