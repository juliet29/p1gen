from pathlib import Path
from replan2eplus.campaigns.decorator2 import make_experimental_campaign
from replan2eplus.campaigns.inputs.data import make_data_dict
from replan2eplus.campaigns.inputs.defn import SampleDef
from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.ezcase.main import EZCase
from replan2eplus.ezobjects.construction import EPConstructionSet

# TODO read details from elsewhere ..  => and they should take a variable..
from replan2eplus.ops.afn.utils import update_vent_schedule_for_select_afn_surfaces
from replan2eplus.ops.subsurfaces.interfaces import (
    Detail,
    Dimension,
    EdgeGroup,
    Location,
    SubsurfaceInputs2,
)
from replan2eplus.ops.zones.interfaces import Room
from replan2eplus.paths import CAMPAIGN_TESTS, PATH_TO_WEATHER_FILE


def create_details(window_dimension: Dimension):
    return {
        "door": Detail(
            window_dimension, Location("mm", "CENTROID", "CENTROID"), "Door"
        ),
        "window": Detail(
            Dimension(1, 2), Location("mm", "CENTROID", "CENTROID"), "Window"
        ),
    }


def create_constructions_set(material_type):
    return EPConstructionSet()


# TODO: the definition of "run simple ezcase has to match the data dict variables -> can this be assured?"
@make_experimental_campaign(
    SampleDef().definition_dict, make_data_dict(), root_path=CAMPAIGN_TESTS
)
def generate_experiments(
    rooms: list[Room],
    connections: list[EdgeGroup],
    window_dimension: Dimension,
    material_type,
    afn_subsurface_select_fx,
    vent_schedule,
    out_path: Path,
):
    details = create_details(window_dimension)
    ss_input = SubsurfaceInputs2(connections, details)
    construction_set = create_constructions_set(material_type)

    print("Starting to create case!")
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(rooms)
    # case.add_airboundaries()

    case.add_subsurfaces(
        ss_input
    )  # TODO should this not handle the airboundaries? or automatically select the approp airboundary edges..

    case.add_constructions_from_other_idf(
        EP_PATHS.construction_paths.constructiin_idfs,
        EP_PATHS.construction_paths.material_idfs,
        construction_set,
    )
    case.add_airflownetwork()  # TODO should take in venting schedules object and object this should be applied to
    update_vent_schedule_for_select_afn_surfaces(
        case.idf, case.airflownetwork, afn_subsurface_select_fx, vent_schedule
    )
    case.save_and_run_case(path_=out_path, RUN=False)
    print("Done creating case!")


if __name__ == "__main__":
    generate_experiments("", "", "", "")
