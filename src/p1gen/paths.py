from typing import Literal
from utils4plans.paths import StaticPaths
import pyprojroot
from pathlib import Path
from dataclasses import dataclass
from utils4plans.io import read_json


# external paths -> TODO put this in a config file??
ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
PATH_TO_IDD = ENERGY_PLUS_LOCATION / "Energy+.idd"

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", BASE_PATH)  # TODO can extend static paths if like..

## reading idfs..
MATERIALS_EXP = static_paths.models / "material_exp"
test_case = (
    MATERIALS_EXP / "Medium_case_bol_5"
)  # "Medium_case_amb_b1"  # Medium_case_red_b1 # Medium_case_bol_5
IDF_NAME = "out.idf"
PATH_TO_SQL_SUBPATH = "results/eplusout.sql"


## reading in plans
SVG2PLANS = static_paths.plans / "svg2plan_outputs_p1gen"
test_plan = SVG2PLANS / "case_bol_5"

# test_plan = SVG2PLANS / "case_red_b1"
# test_plan = SVG2PLANS / "case_amb_b1"


# replan tests
REPLAN2EPLUS_TESTS = static_paths.models / "replan_test"
EXP_NAMES = Literal["case_bol_5", "case_red_b1", "case_amb_b1"]


# can access results via REPLAN2EPLUS_TESTS / <one in EXP_NAMES>
def get_result_path(exp: EXP_NAMES):
    return REPLAN2EPLUS_TESTS / exp


THROWAWAY_PATH = BASE_PATH / "throwaway"


@dataclass
class PlanPaths:
    path_to_case: Path

    PLAN_JSON_NAME = "plan"
    EDGES_NAME = "graph"
    DESIGN_DETAILS_NAME = "subsurfaces"

    @property
    def plan(self):
        return read_json(self.path_to_case, self.PLAN_JSON_NAME)

    @property
    def edges(self):
        return read_json(self.path_to_case, self.EDGES_NAME)

    @property
    def design_details(self):
        return read_json(self.path_to_case, self.DESIGN_DETAILS_NAME)


path_to_test_plan = PlanPaths(test_plan)

if __name__ == "__main__":
    print(MATERIALS_EXP)

STATIC_PATH = Path(
    "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/static/_01_inputs"
)

PATH_TO_WINDOW_GAS_IDF = STATIC_PATH / "constructions/WindowGasMaterials.idf"
PATH_TO_WINDOW_GLASS_IDF = STATIC_PATH / "constructions/WindowGlassMaterials.idf"
PATH_TO_MAT_AND_CONST_IDF = STATIC_PATH / "constructions/ASHRAE_2005_HOF_Materials.idf"

material_idfs = [
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_GAS_IDF,
]
PATH_TO_WINDOW_CONST_IDF = STATIC_PATH / "constructions/WindowConstructs.idf"
PATH_TO_WEATHER_FILE = STATIC_PATH / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
PATH_TO_MINIMAL_IDF = STATIC_PATH / "base/01example/Minimal_AP.idf"
