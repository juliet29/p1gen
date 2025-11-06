from matplotlib.axes import Axes
from p1gen._03_execute.assemble import ComparisonData, assemble_comparison_data
from rich import print
from replan2eplus.ex.make import make_data_plot
from replan2eplus.ezcase.ez import EZ
from replan2eplus.results.sql import get_qoi
from replan2eplus.visuals.data.data_plot import DataPlot
from replan2eplus.visuals.data.colorbars import pressure_colorbar
import matplotlib.cm as cm
from p1gen.paths import Constants
from tabulate import tabulate

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def study_pressure_data(hour=12):
    comp_data = assemble_comparison_data("20251105_door_sched").default_experiments
    noon_pressures = [
        get_qoi("AFN Node Total Pressure", i.path).select_time(hour) for i in comp_data
    ]
    quantiles = [i.quantile(q=[0.1, 0.25, 0.75, 0.9]).data for i in noon_pressures]

    print(tabulate(quantiles))
    return noon_pressures


def create_pressue_geometry_plot(
    comparison: ComparisonData, fig: Figure, ax: Axes, hour=12
):
    path = comparison.path
    case = comparison.ezcase
    pressure = get_qoi("AFN Node Total Pressure", path)
    data_at_noon = pressure.select_time(hour)
    # print(data_at_noon)

    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", path)
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", path)
    combined_flow = flow_12.select_time(hour) - flow_21.select_time(hour)
    # print(combined_flow)

    dp = DataPlot(case.objects.zones, cardinal_expansion_factor=2)
    dp.fig = fig
    dp.axes = ax

    dp.set_geometry_color_maps(data_at_noon, min_=-3, max_=-1.5)
    dp.data_array = data_at_noon
    # dp.geom_bar, dp.geom_cmap, dp.geom_norm = pressure_colorbar(
    #     dp.data_array.values, dp.axes, min_=-2, max_=-0.1
    # )

    dp.plot_zone_names()
    dp.plot_zones_with_data()
    dp.plot_cardinal_names_with_data()
    dp.plot_subsurfaces_and_surfaces(
        case.objects.airflow_network,
        case.objects.airboundaries,
        case.objects.subsurfaces,
    )
    dp.plot_connections_with_data(
        combined_flow, case.objects.subsurfaces, case.objects.airboundaries
    )
    dp.set_limits()
    return dp


def create_geometry_plots():
    comp_data = assemble_comparison_data("20251105_door_sched")
    # print([i.case for i in comp_data.values])
    exp0, exp1, exp2 = comp_data.default_experiments

    fig, (ax0, ax1, ax2, ax3) = plt.subplots(ncols=4, figsize=(24, 10))
    dp = create_pressue_geometry_plot(exp0, fig, ax0)
    dp = create_pressue_geometry_plot(exp1, fig, ax1)
    dp = create_pressue_geometry_plot(exp2, fig, ax2)

    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=dp.geom_norm, cmap=dp.geom_cmap),
            orientation="vertical",
            label="Total Pressure [Pa]",
            ax=ax3,
            # shrink=0.5
            # TODO pass in the label
        ),
    )
    # dp.show()
    plt.show()


if __name__ == "__main__":
    create_geometry_plots()
    # res = study_pressure_data()
