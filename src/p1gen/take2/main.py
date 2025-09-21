from pathlib import Path
from p1gen.take2.interfaces import Plan
from p1gen.take2.subsurface_interfaces import EdgesList, DesignDetails
from p1gen.paths import PlanPaths, THROWAWAY_PATH, path_to_test_plan
from pydantic import ValidationError
from replan2eplus.subsurfaces.interfaces import SubsurfaceInputs
from replan2eplus.ezcase.main import EZCase
from replan2eplus.examples.mat_and_const import SAMPLE_CONSTRUCTION_SET
from replan2eplus.visuals.base_plot import BasePlot

from replan2eplus.examples.defaults import PATH_TO_IDD


from rich import print

# TODO make these paths actually static.. not based on the .git only.. handling paths in packages..
STATIC_PATH = Path(
    "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/static/_01_inputs"
)


PATH_TO_MINIMAL_IDF = STATIC_PATH / "base/01example/Minimal_AP.idf"

PATH_TO_WEATHER_FILE = STATIC_PATH / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"

PATH_TO_MAT_AND_CONST_IDF = STATIC_PATH / "constructions/ASHRAE_2005_HOF_Materials.idf"
PATH_TO_WINDOW_CONST_IDF = STATIC_PATH / "constructions/WindowConstructs.idf"

PATH_TO_WINDOW_GLASS_IDF = STATIC_PATH / "constructions/WindowGlassMaterials.idf"
PATH_TO_WINDOW_GAS_IDF = STATIC_PATH / "constructions/WindowGasMaterials.idf"

material_idfs = [
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_GAS_IDF,
]


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


def prep_subsurface_inputs(path_to_plan: PlanPaths):
    design_details = read_details(path_to_plan)
    edges_data = read_edges(path_to_plan)
    airboundary_edges = edges_data.airboundary_edges
    details = design_details.details_map
    subsurface_edges = edges_data.true_subsurfaces_dict_as_edges
    map_ = edges_data.make_updated_map(design_details)

    return airboundary_edges, SubsurfaceInputs(subsurface_edges, details, map_)
    # TODO: need to update this replan2eplus for the IndexPair update to work..


def plot_base_case(case: EZCase):
    bp = (
        BasePlot(case.zones, cardinal_expansion_factor=1.4)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal_names()
        .plot_subsurfaces_and_surfaces(
            case.airflownetwork, case.unique_airboundaries, case.unique_subsurfaces
        )
        .plot_connections(
            case.airflownetwork, case.unique_airboundaries, case.unique_subsurfaces
        )
    )
    bp.show()


def prep_case(path_to_plan: PlanPaths, output_path = THROWAWAY_PATH):
    rooms = read_plan(path_to_plan)
    airboundary_edges, subsurface_details = prep_subsurface_inputs(path_to_plan)

    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(rooms)
    case.add_airboundaries(airboundary_edges)
    case.add_subsurfaces(subsurface_details)

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    case.add_airflownetwork()


    case.save_and_run_case(output_path)

    return case


if __name__ == "__main__":
    prep_case(path_to_test_plan)
    # read_details()
    # prep_subsurface_inputs()
