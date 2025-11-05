from typing import Literal, get_args

from replan2eplus.ops.schedules.interfaces.year import create_year_from_single_value
from replan2eplus.prob_door.functions import create_venting_year
from replan2eplus.prob_door.interfaces import VentingState
from replan2eplus.campaigns.decorator2 import DataDict
from replan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup
from replan2eplus.ops.zones.user_interface import Room
from replan2eplus.ops.afn.user_interface import AFNVentingInput, AFNInput

from p1gen.generate.construction_sets import MaterialTypes, create_constructions_sets
from p1gen.paths import EXP_NAMES, PlanPaths
from p1gen.readin.read import read_details, read_edges, read_plan


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


def generate_airboundary_edges():
    def get_ab_edges_for_plan(name):
        edge_list = read_edges(PlanPaths(name))
        return edge_list.airboundary_edges

    return {v: get_ab_edges_for_plan(k) for k, v in EXP_NAME_MAP.items()}


def generate_window_dimensions():
    details = read_details(PlanPaths("case_amb_b1")).windows_dict["Window_1"]
    default_dim = details.dimension
    mod = 0.3
    min_dim = default_dim.modify_area(1 - mod)
    max_dim = default_dim.modify_area(1 + mod)
    return {"-30%": min_dim, "Default": default_dim, "+30%": max_dim}


def generate_construction_sets():
    material_types = get_args(MaterialTypes)
    return {k: create_constructions_sets(k) for k in material_types}


def generate_door_venting_schedules():
    closed_year = create_year_from_single_value(VentingState.CLOSE.value)
    closed_vent = AFNInput([AFNVentingInput("Doors", closed_year)])
    dynamic_vent = AFNInput([AFNVentingInput("Doors", create_venting_year())])
    open_vent = AFNInput([])

    return {
        "Always Closed": closed_vent,
        "Dynamic": dynamic_vent,
        "Always Open": open_vent,
    }


campaign_data = DataDict(
    case={
        "rooms": generate_rooms(),
        "edge_groups": generate_edge_groups(),
        "airboundary_edges": generate_airboundary_edges(),
    },
    mods={
        "window_dimension": generate_window_dimensions(),
        "door_vent_schedule": generate_door_venting_schedules(),
        "construction_set": generate_construction_sets(),
    },
)
