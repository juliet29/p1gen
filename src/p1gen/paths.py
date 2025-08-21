from utils4plans.paths import StaticPaths
import pyprojroot
from pathlib import Path

# external paths -> TODO put this in a config file??
ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
PATH_TO_IDD = ENERGY_PLUS_LOCATION / "Energy+.idd"

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", BASE_PATH) #TODO can extend static paths if like.. 


MATERIALS_EXP = static_paths.models / "material_exp"
test_case = MATERIALS_EXP / "Medium_case_bol_5" #"Medium_case_amb_b1"


IDF_NAME = "out.idf"
PATH_TO_SQL_SUBPATH = "results/eplusout.sql"


if __name__ == "__main__":
    print(MATERIALS_EXP)
