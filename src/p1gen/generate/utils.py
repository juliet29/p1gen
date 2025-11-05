from replan2eplus.ops.subsurfaces.interfaces import Dimension
from replan2eplus.ops.subsurfaces.user_interfaces import Detail
from p1gen.paths import PlanPaths
from p1gen.readin.read import read_details


def get_details():
    return read_details(PlanPaths("case_amb_b1")).details_dict


def create_details(window_dimension: Dimension) -> dict[str, Detail]:
    details = get_details()
    window_details = details["Window_1"]
    new_window_details = Detail(
        window_dimension, window_details.location, window_details.type_
    )
    details["Window_1"] = new_window_details
    return details
