from typing import Literal
from replan2eplus.ezcase.ez import EZ
from utils4plans.paths import StaticPaths
import pyprojroot
from pathlib import Path
from dataclasses import dataclass
from utils4plans.io import read_json
from replan2eplus.paths import load_ep_paths
from replan2eplus.results.sql import get_sql_results

# TODO -> these go in a config .. -> only put things you want users to be able to change into a config

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", BASE_PATH)  # TODO can extend static paths if like..
ep_paths = load_ep_paths()
ep_paths.reset_minimal_case(static_paths.inputs / "Minimal_AP.idf")

EXP_NAMES = Literal["case_bol_5", "case_red_b1", "case_amb_b1"]

CampaignNameOptions = Literal[
    "20251019_",
    "20251020_NoAFN",
    "20251105_door_sched",
    "20251109_summer",
    "20251112_summer_update_dv",
    "test",
    "20251116_palo_alto",
]


FigureNames = Literal["pressure_geom", "time_box", "test", "sensitivity_line"]


class Constants:
    IDF_NAME = "out.idf"
    RESULTS_DIR = "results"
    PATH_TO_SQL = f"{RESULTS_DIR}/eplusout.sql"
    DEFAULT_OPTION = "Default"
    DEFAULT_CATEGORY = "Default"
    METADATA = "metadata.toml"
    DEFINITION = "defn.toml"


class DynamicPaths:
    MATERIALS_EXP = static_paths.models / "material_exp"
    test_case = MATERIALS_EXP / "Medium_case_bol_5"

    SVG2PLANS = static_paths.plans / "svg2plan_outputs_p1gen"
    test_plan = SVG2PLANS / "case_bol_5"
    REPLAN2EPLUS_TESTS = static_paths.models / "replan_test"
    CAMPAIGN = static_paths.models / "campaigns"
    THROWAWAY_PATH = BASE_PATH / "throwaway"
    PALOALTO23 = static_paths.inputs / "CA_PALO-ALTO-AP_724937_23.EPW"

    def get_path_for_comparison_data(
        self, campaign: CampaignNameOptions, qoi: Literal["temperature", "ach"]
    ):
        path = (
            static_paths.temp / campaign / "comparisons" / f"{qoi}.csv"
        )  # there are different units -> temp vs other, so concat this.. for now just temp..
        return path


@dataclass
class PlanPaths:
    case_name: EXP_NAMES
    case_folder: Path = DynamicPaths.SVG2PLANS
    PLAN_JSON_NAME = "plan"
    EDGES_NAME = "graph"
    DESIGN_DETAILS_NAME = "subsurfaces"

    @property
    def path_to_case(self):
        return self.case_folder / self.case_name

    @property
    def plan(self):
        return read_json(self.path_to_case, self.PLAN_JSON_NAME)

    @property
    def edges(self):
        return read_json(self.path_to_case, self.EDGES_NAME)

    @property
    def design_details(self):
        return read_json(self.path_to_case, self.DESIGN_DETAILS_NAME)


def get_sqlite_object(path: Path):
    try:
        return get_sql_results(path)
    except AssertionError:
        raise Exception(
            f"Could not find sql results for {path.parent.name} / {path.name}"
        )


def get_ezcase_for_path(path: Path):
    try:
        pname = path / Constants.IDF_NAME
        assert pname.exists()
    except AssertionError:
        raise Exception(
            f"Could not find name {Constants.IDF_NAME} at {path.parent.name} / {path.name}"
        )

    return EZ(path / Constants.IDF_NAME)


if __name__ == "__main__":
    print(DynamicPaths.MATERIALS_EXP)
