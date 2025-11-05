# from replan2eplus.ex.make import make_test_case
from pathlib import Path
from p1gen.generate.utils import create_details
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.afn.user_interface import AFNInput
from replan2eplus.ops.subsurfaces.ezobject import Edge as ReplanEdge
from replan2eplus.ops.subsurfaces.interfaces import Dimension
from replan2eplus.ops.subsurfaces.user_interfaces import (
    EdgeGroup,
    SubsurfaceInputs,
)
from replan2eplus.ops.zones.user_interface import Room
from replan2eplus.paths import ep_paths
from rich import print

from p1gen.generate.data_dict import (
    campaign_data,
    generate_door_venting_schedules,
    generate_window_dimensions,
)
from p1gen.paths import DynamicPaths


def make_test_case(
    rooms: list[Room],
    edge_groups: list[EdgeGroup],
    airboundary_edges: list[ReplanEdge],
    window_dimension: Dimension,
    door_vent_schedule: AFNInput,
    out_path: Path,
):
    details = create_details(window_dimension)
    ss_input = SubsurfaceInputs(edge_groups, details)

    case = EZ(epw_path=ep_paths.default_weather, output_path=out_path)
    case.add_zones(rooms)

    case.add_subsurfaces(ss_input, airboundary_edges=airboundary_edges)

    case.add_airflow_network(door_vent_schedule)

    case.add_constructions()
    return case


def test_vent_sched():
    campaign_case_data = campaign_data.case
    case_a_data = [v["A"] for k, v in campaign_case_data.items()]
    rooms, edge_groups, airboundary_edges = case_a_data
    vent_scheds = generate_door_venting_schedules()
    window_dims = generate_window_dimensions()

    curr_sched = vent_scheds["Always Closed"]
    curr_dim = window_dims["Default"]

    case = make_test_case(
        rooms=rooms,
        edge_groups=edge_groups,
        airboundary_edges=airboundary_edges,
        window_dimension=curr_dim,
        door_vent_schedule=curr_sched,
        out_path=DynamicPaths.THROWAWAY_PATH,
    )

    case.save_and_run(run=False)


if __name__ == "__main__":
    test_vent_sched()
