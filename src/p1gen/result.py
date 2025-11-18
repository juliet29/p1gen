# from p1gen.time_period.dist import make_box_charts
# from p1gen.geom.geom import create_geometry_plots
# from p1gen.sensitivity.plot import make_sensitivity_temp_plot
from p1gen.config import CURRENT_CAMPAIGN
from p1gen.sensitivity.plot import make_sensitivity_flow_plot


def create_figures():
    pass
    # make_box_charts()
    # make_sensitivity_temp_plot(CURRENT_CAMPAIGN)
    # create_geometry_plots(CURRENT_CAMPAIGN)
    # prep_weather_plots()


def create_second_round_figs():
    make_sensitivity_flow_plot(CURRENT_CAMPAIGN)


if __name__ == "__main__":
    # create_figures()
    create_second_round_figs()
