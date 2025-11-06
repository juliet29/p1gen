from typing import Literal
from utils4plans.paths import StaticPaths
import pyprojroot
from pathlib import Path
from dataclasses import dataclass
from utils4plans.io import read_json
from replan2eplus.paths import load_ep_paths

# TODO -> these go in a config .. -> only put things you want users to be able to change into a config

EXP_NAMES = Literal["case_bol_5", "case_red_b1", "case_amb_b1"]
CampaignNameOptions = Literal["20251019_", "20251020_NoAFN", "20251105_door_sched"]


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", BASE_PATH)  # TODO can extend static paths if like..
ep_paths = load_ep_paths()
ep_paths.reset_minimal_case(static_paths.inputs / "Minimal_AP.idf")


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


def get_result_path(exp: EXP_NAMES):
    return DynamicPaths.REPLAN2EPLUS_TESTS / exp


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


path_to_test_plan = PlanPaths("case_bol_5")


if __name__ == "__main__":
    print(DynamicPaths.MATERIALS_EXP)

# STATIC_PATH = Path(
#     "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/static/_01_inputs"
# )

# PATH_TO_WINDOW_GAS_IDF = STATIC_PATH / "constructions/WindowGasMaterials.idf"
# PATH_TO_WINDOW_GLASS_IDF = STATIC_PATH / "constructions/WindowGlassMaterials.idf"
# PATH_TO_MAT_AND_CONST_IDF = STATIC_PATH / "constructions/ASHRAE_2005_HOF_Materials.idf"

# material_idfs = [
#     PATH_TO_MAT_AND_CONST_IDF,
#     PATH_TO_WINDOW_GLASS_IDF,
#     PATH_TO_WINDOW_GAS_IDF,
# ]
# PATH_TO_WINDOW_CONST_IDF = STATIC_PATH / "constructions/WindowConstructs.idf"
# PATH_TO_WEATHER_FILE = STATIC_PATH / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
# PATH_TO_MINIMAL_IDF = STATIC_PATH / "base/01example/Minimal_AP.idf"
