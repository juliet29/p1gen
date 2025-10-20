from pathlib import Path

from replan2eplus.campaigns.decorator2 import make_experimental_campaign
from replan2eplus.ezcase.main import EZCase
from replan2eplus.ezobjects.construction import EPConstructionSet

from replan2eplus.ops.subsurfaces.interfaces import (
    Detail,
    Dimension,
    EdgeGroup,
    SubsurfaceInputs2,
)
from replan2eplus.ops.zones.interfaces import Room

from p1gen.generate.data_dict import exp_data, get_details
from p1gen.generate.defn_dict import defn
from p1gen.paths import ep_paths, DynamicPaths
from replan2eplus.ezobjects.subsurface import Edge as ReplanEdge


def create_details(window_dimension: Dimension) -> dict[str, Detail]:
    details = get_details()
    window_details = details["Window_1"]
    new_window_details = Detail(
        window_dimension, window_details.location, window_details.type_
    )
    details["Window_1"] = new_window_details
    return details


# TODO: the definition of "run simple ezcase has to match the data dict variables -> can this be assured?"
@make_experimental_campaign(
    defn, exp_data, root_path=DynamicPaths.CAMPAIGN, campaign_name="NoAFN"
)
def generate_experiments(
    rooms: list[Room],
    edge_groups: list[EdgeGroup],
    airboundary_edges: list[ReplanEdge],
    window_dimension: Dimension,
    construction_set: EPConstructionSet,
    # afn_subsurface_select_fx,
    # vent_schedule,
    out_path: Path,
):
    details = create_details(window_dimension)
    ss_input = SubsurfaceInputs2(edge_groups, details)

    print("Starting to create case!")

    case = EZCase(
        ep_paths.idd_path, ep_paths.default_minimal_case, ep_paths.default_weather
    )
    case.initialize_idf()
    case.add_zones(rooms)
    case.add_airboundaries(airboundary_edges) # skipping for now.

    case.add_subsurfaces(ss_input)

    case.add_constructions_from_other_idf(
        ep_paths.construction_paths.constructiin_idfs,
        ep_paths.construction_paths.material_idfs,
        construction_set,
    )
    case.add_airflownetwork()

    # skipping for now..
    # update_vent_schedule_for_select_afn_surfaces(
    #     case.idf, case.airflownetwork, afn_subsurface_select_fx, vent_schedule
    # )
    case.add_output_variables()
    case.save_and_run_case(path_=out_path, RUN=False)
    print("Done creating case!")


if __name__ == "__main__":
    generate_experiments([], [], "", "", "")  # type: ignore
