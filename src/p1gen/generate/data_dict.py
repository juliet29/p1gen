from replan2eplus.campaigns.decorator2 import DataDict
from p1gen.generate.construction_sets import MaterialTypes, create_constructions_sets
from p1gen.readin.read import read_plan, read_edges, read_details
from p1gen.paths import PlanPaths, EXP_NAMES
from typing import Literal, NamedTuple, TypedDict, get_args
from replan2eplus.ops.zones.interfaces import Room

from replan2eplus.ops.subsurfaces.interfaces import EdgeGroup

exp_synonyms = Literal["A", "B", "C"]

EXP_NAME_MAP: dict[EXP_NAMES, exp_synonyms] = {
    "case_amb_b1": "A",
    "case_bol_5": "B",
    "case_red_b1": "C",
}

DetailNames = Literal["Door_1", "Window_1"]


def generate_rooms() -> dict[str, list[Room]]:
    return {v: read_plan(PlanPaths(k)) for k, v in EXP_NAME_MAP.items()}


def generate_edge_groups_for_plan(name: EXP_NAMES):
    edge_list = read_edges(PlanPaths(name))
    door_edges = edge_list.create_edge_group(
        edge_list.internal_edges, "Door_1", "Zone_Zone"
    )
    window_edges = edge_list.create_edge_group(
        edge_list.external_edges, "Window_1", "Zone_Direction"
    )
    return [door_edges, window_edges]


def generate_edge_groups() -> dict[str, list[EdgeGroup]]:
    return {v: generate_edge_groups_for_plan(k) for k, v in EXP_NAME_MAP.items()}


def get_details():
    return read_details(PlanPaths("case_amb_b1")).details_dict


def generate_window_dimensions():
    details = read_details(PlanPaths("case_amb_b1")).windows_dict["Window_1"]
    default_dim = details.dimension
    mod = 0.3
    min_dim = default_dim.modify_area(1 - mod)
    max_dim = default_dim.modify_area(1 + mod)
    return {"-30%": min_dim, "Default": default_dim, "+30%": max_dim}


def generate_construction_sets():
    mtypes = get_args(MaterialTypes)
    return {k: create_constructions_sets(k) for k in mtypes}


exp_data = DataDict(
    case={
        "rooms": generate_rooms(),
        "edge_groups": generate_edge_groups(),
    },
    mods={
        "window_dimension": generate_window_dimensions(),
        # "door_vent_schedule": {"Always Closed": 0, "Dynamic": 0, "Always Open": 0},
        "construction_set": generate_construction_sets(),
    },
)
