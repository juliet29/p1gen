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
test_plan = SVG2PLANS / "case_amb_b1"


@dataclass
class PlanPaths:
    path_to_case: Path

    PLAN_JSON_NAME = "plan"
    EDGES_NAME = "graph"
    SUBSURFACES_NAME = "subsurfaces"

    @property
    def plan(self):
        return read_json(self.path_to_case, self.PLAN_JSON_NAME)

test_plan_paths = PlanPaths(test_plan)

if __name__ == "__main__":
    print(MATERIALS_EXP)
