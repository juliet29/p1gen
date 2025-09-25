from pathlib import Path
import polars as pl
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.results.sql import get_sql_results
import xarray as xr


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


def prep_case(
    path_to_idd: Path,
    path_to_case: Path,
):
    case = ExistCase(path_to_idd, path_to_case / "out.idf")
    sql_results = get_sql_results(path_to_case)
    return case, sql_results
