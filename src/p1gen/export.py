from p1gen.paths import MATERIALS_EXP, static_paths
from p1gen.volume import make_plots_by_zone
from utils4plans.io import get_or_make_folder_path

case_paths = [
    MATERIALS_EXP / "Medium_case_bol_5",
    MATERIALS_EXP / "Medium_case_amb_b1",
    MATERIALS_EXP / "Medium_case_red_b1",
]


def save_time_graphs():
    for path in case_paths:
        vol_chart, heat_chart = make_plots_by_zone(path)
        dir = get_or_make_folder_path(static_paths.figures, path.name)
        vol_name, heat_name = "vol.png", "heat.png"
        vol_chart.save(dir / vol_name, "png")
        heat_chart.save(dir / heat_name, "png")

if __name__ == "__main__":
    save_time_graphs()