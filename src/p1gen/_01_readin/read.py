from pydantic import ValidationError

from p1gen.paths import PlanPaths
from p1gen._01_readin.interfaces import Plan
from p1gen._01_readin.subsurface_interfaces import DesignDetails, EdgesList


def read_plan(path_to_plan: PlanPaths):
    json_data = path_to_plan.plan[
        0
    ]  # TODO STOP DOUBLE NESTING PLAN.JSON IN SVG2PLAN! -> instead update to have "rooms" as a part!
    try:
        plan_data = Plan.model_validate({"rooms": json_data})
    except ValidationError as e:
        raise Exception(f"Plan at {path_to_plan.path_to_case} has invalid data: {e}")
    return plan_data.replan2eplus_rooms


def read_edges(path_to_plan: PlanPaths):  # TODO wrap all in a try-catch..
    json_data = path_to_plan.edges
    edges_data = EdgesList.model_validate(json_data)
    # print(edges_data)
    return edges_data


def read_details(path_to_plan: PlanPaths):
    json_data = path_to_plan.design_details
    details_data = DesignDetails.model_validate(json_data)
    # print(details_data)
    return details_data


# def prep_subsurface_inputs(path_to_plan: PlanPaths):
#     design_details = read_details(path_to_plan)
#     edges_data = read_edges(path_to_plan)
#     airboundary_edges = edges_data.airboundary_edges
#     details = design_details.details_map
#     subsurface_edges = edges_data.true_subsurfaces_dict_as_edges
#     map_ = edges_data.make_updated_map(design_details)

#     return airboundary_edges, SubsurfaceInputs(subsurface_edges, details, map_)
