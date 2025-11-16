from p1gen.time_period.plot import get_data_and_make_plots as save_boxplot
from p1gen._04_single_day.geom import create_geometry_plots
from p1gen._05_sensitivity.plot import make_sensitivity_plot
from p1gen.config import CURRENT_CAMPAIGN


def create_figures():
    save_boxplot(CURRENT_CAMPAIGN)
    make_sensitivity_plot(CURRENT_CAMPAIGN)
    create_geometry_plots(CURRENT_CAMPAIGN)


if __name__ == "__main__":
    create_figures()
