from copy import deepcopy
from enum import StrEnum
from typing import Optional

import polars as pl
from geomeppy import IDF
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.ezobjects.subsurface import Subsurface

from p1gen.read_sql import (
    SpaceTypes,
    SQLCollection,
    SQLiteResult,
    create_collections_for_variable,
)
from p1gen.utils import CurrCase
from p1gen.utils import get_zone_by_name, get_surface_by_name, get_surface_or_subsuface_by_name


# class DFC(StrEnum):

class DFC:
    """Dataframe Columns"""
    CASE_NAMES = "case_names"
    SPACE_NAMES = "space_names"

    DATETIMES = "datetimes"
    HOUR = "hour"
    TIME = "time"

    ZONE = "zone"
    DIRECTION = "direction"
    IS_EXTERIOR = "is_exterior"

def extend_data(val, len_data):
    return [val] * len_data


def add_space_name_details(
    geom: Zone | Surface | Subsurface, _data_dict: dict[str, list], len_data: int
):
    def handle_surface(surf):
        data_dict[DFC.DIRECTION] = extend_data(surf.direction.name, len_data)
        is_exterior = surf.boundary_condition == "outdoors"
        data_dict[DFC.IS_EXTERIOR] = extend_data(is_exterior, len_data)
        return data_dict

    data_dict = deepcopy(_data_dict)
    if isinstance(geom, Surface):
        return handle_surface(geom)
    if isinstance(geom, Subsurface):
        return handle_surface(geom.surface)

    # its a zone 
    data_dict[DFC.ZONE] = extend_data(geom.zone_name, len_data)
    return data_dict


def handle_add_space_name_details(
    collection: SQLCollection,
    data_dict: dict[str, list],
    case: CurrCase,
    # idf: IDF,
):
    # TODO write tests for different speace types!
    pass
    match collection.space_type:
        case SpaceTypes.ZONE.value:
            geom = get_zone_by_name(collection.space_name, case.zones)

        case SpaceTypes.SYSTEM.value:
            geom = get_zone_by_name(collection.space_name, case.zones)
            if not geom:
                geom = get_surface_or_subsuface_by_name(collection.space_name, case.subsurfaces + case.surfaces)
            if not geom:
                pass
                # cant add any additional attributes, bc not associated with a geometry 
                return data_dict    

        case SpaceTypes.SURFACE.value:
            geom = get_surface_by_name(collection.space_name, case.surfaces)
            if not geom: 
                return data_dict
        case _:
            raise NotImplementedError(
                f"Havent handled this type of surface..{collection.space_type} "
            )
    len_data = len(collection.values)
    assert geom
    return add_space_name_details(geom, data_dict, len_data)


def create_long_dataframe(
    collection: SQLCollection,
    case: CurrCase,
):
    len_data = len(collection.values)
    data_dict: dict[str, list] = {}

    if case.case_name:
        data_dict[DFC.CASE_NAMES] = extend_data(case.case_name, len_data)

    data_dict[DFC.SPACE_NAMES] = extend_data(collection.space_name, len_data)

    if collection.space_type != SpaceTypes.SITE:
        data_dict = handle_add_space_name_details(collection, data_dict, case)

    data_dict[DFC.DATETIMES] = list(collection.datetimes)

    return pl.DataFrame(data_dict).with_columns(
        pl.Series(name=collection.qoi, values=collection.values)
    )


def dataframe_for_qoi(
    sql: SQLiteResult,
    qoi: str,
    case: CurrCase,
):
    collections = create_collections_for_variable(sql, qoi)
    # TODO can do the opposte -> set a flag 
    valid_collections = [i for i in collections if i.space_name in case.geom_names]
    non_zero_collections = [i for i in valid_collections if any(i.values)]

    dataframes = [create_long_dataframe(collection, case) for collection in non_zero_collections]
    # split dataframes based on their shape.. 
    df1 = pl.concat(dataframes, how="vertical_relaxed")
    return df1


def create_dataframe_for_case(
    sql: SQLiteResult,
    qois: list[str],
    case: CurrCase,
):
    df0 = dataframe_for_qoi(sql, qois[0], case)
    if len(qois) == 1:
        return df0
    remaining_dfs = [dataframe_for_qoi(sql, qoi, case) for qoi in qois[1:]]
    # collections = create_collections_for_variable(sql, qois[0])
    # dataframes = [
    #     create_long_dataframe(collection, idf, case_name) for collection in collections
    # ]
    # df0 = pl.concat(dataframes, how="vertical")

    # if have many qois.. assume that have matching surface type..
    # df1 = dataframe_for_qoi(sql, qois[1])
    # df2 = dataframe_for_qoi(sql, qois[2])
    # df0.join(df1, on = [DFC.SPACE_NAMES.value, DFC.DATETIMES.value])
    return pl.concat([df0] + remaining_dfs, how="align") # note will get error here for diff space types.. 
