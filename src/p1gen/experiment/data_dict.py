from replan2eplus.campaigns.decorator2 import DataDict
from p1gen.readin.read import read_plan, read_edges
from p1gen.paths import PlanPaths, EXP_NAMES
from typing import Literal, NamedTuple, TypedDict
from replan2eplus.ops.zones.interfaces import Room

from replan2eplus.ops.subsurfaces.interfaces import EdgeGroup

exp_synonyms = Literal["A", "B", "C"]

EXP_NAME_MAP: dict[EXP_NAMES, exp_synonyms] = {
    "case_amb_b1": "A",
    "case_bol_5": "B",
    "case_red_b1": "C",
}

DetailNames = Literal["Door", "Window"]


def generate_rooms() -> dict[str, list[Room]]:
    return {v: read_plan(PlanPaths(k)) for k, v in EXP_NAME_MAP.items()}


def generate_edge_groups_for_plan(name: EXP_NAMES):
    edge_list = read_edges(PlanPaths(name))
    door_edges = edge_list.create_edge_group(
        edge_list.internal_edges, "Door", "Zone_Zone"
    )
    window_edges = edge_list.create_edge_group(
        edge_list.external_edges, "Window", "Zone_Direction"
    )
    return [door_edges, window_edges]


def generate_edge_groups() -> dict[str, list[EdgeGroup]]:
    return {v: generate_edge_groups_for_plan(k) for k, v in EXP_NAME_MAP.items()}


exp_data = DataDict(
    case={
        "rooms": generate_rooms(),
        "edge_groups": generate_edge_groups(),
    },
    mods={
        "window_dim": {"-50%": 0, "Default": 0, "+50%": 0},
        "door_vent_schedule": {"Always Closed": 0, "Dynamic": 0, "Always Open": 0},
        "construction": {"Light": 0, "Medium": 0, "Heavy": 0},
    },
)
