from pathlib import Path

from replan2eplus.campaigns.decorator2 import make_experimental_campaign
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.afn.user_interface import AFNInput
from replan2eplus.ops.constructions.interfaces import EPConstructionSet
from replan2eplus.ops.constructions.user_interface import ConstructionInput
from replan2eplus.ops.subsurfaces.ezobject import Edge as ReplanEdge
from replan2eplus.ops.subsurfaces.interfaces import Dimension
from replan2eplus.ops.subsurfaces.user_interfaces import (
    EdgeGroup,
    SubsurfaceInputs,
)
from replan2eplus.ops.zones.user_interface import Room
from replan2eplus.paths import ep_paths

from p1gen.generate.data_dict import campaign_data
from p1gen.generate.defn_dict import campaign_defn
from p1gen.generate.utils import create_details
from p1gen.paths import DynamicPaths


# TODO: the definition of "run simple ezcase has to match the data dict variables -> can this be assured?"
@make_experimental_campaign(
    campaign_defn,
    campaign_data,
    root_path=DynamicPaths.CAMPAIGN,
    campaign_name="door_sched",
)
def generate_experiments(
    rooms: list[Room],
    edge_groups: list[EdgeGroup],
    airboundary_edges: list[ReplanEdge],
    window_dimension: Dimension,
    door_vent_schedule: AFNInput,
    construction_set: EPConstructionSet,
    out_path: Path,
):
    details = create_details(window_dimension)
    ss_input = SubsurfaceInputs(edge_groups, details)

    print("Starting to create case!")

    case = EZ(epw_path=ep_paths.default_weather, output_path=out_path)
    case.add_zones(rooms)

    case.add_subsurfaces(ss_input, airboundary_edges=airboundary_edges)

    case.add_airflow_network(door_vent_schedule)

    case.add_constructions(
        ConstructionInput(
            ep_paths.construction_paths.constructiin_idfs,
            ep_paths.construction_paths.material_idfs,
            construction_set,
        )
    )

    case.save_and_run(run=False)
    print("Done creating case!")


if __name__ == "__main__":
    generate_experiments([], [], [], "", "", "", "") # pyright: ignore[reportArgumentType]
