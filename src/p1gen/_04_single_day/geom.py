from pathlib import Path
from typing import NamedTuple

import matplotlib as mpl
from matplotlib.axes import Axes
import matplotlib.cm as cm
from matplotlib.colors import Colormap, Normalize, SymLogNorm
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from replan2eplus.results.sql import get_qoi
from replan2eplus.visuals.data.many_data_plot import DataPlot
import xarray as xr

from p1gen._03_execute.assemble import ComparisonData, assemble_default_data
from p1gen.paths import get_ezcase_for_path
from p1gen.plot_utils.utils import NamedData


class ColorNorm(NamedTuple):
    cmap: Colormap
    norm: Normalize


def create_pressure_cnorm(hour=12):
    comp_data = assemble_default_data("20251105_door_sched")
    pressures = [
        NamedData(
            i.case_name, get_qoi("AFN Node Total Pressure", i.path).select_time(hour)
        )
        for i in comp_data
    ]

    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in pressures})
    arr = ds.to_array()
    var_coords = {"variable": ["A", "B", "C"]}
    arr = ds.to_array().assign_coords(var_coords)

    colormap = mpl.colormaps["RdYlBu_r"]
    min_, max_ = arr.min().data, arr.max().data
    norm = SymLogNorm(linthresh=3, linscale=1, vmin=min_, vmax=max_ * 2, base=2)

    return ColorNorm(colormap, norm)


def get_flow_for_path(path: Path, hour: int = 12):
    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", path)
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", path)
    net_flow = flow_12.select_time(hour) - flow_21.select_time(hour)
    return net_flow


def create_flow_cnorm(hour=12, colormap_name: str = "PuBu"):
    comp_data = assemble_default_data("20251105_door_sched")

    flow_data = [
        NamedData(i.case_name, get_flow_for_path(i.path, hour=hour)) for i in comp_data
    ]

    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in flow_data})
    arr = ds.to_array()
    var_coords = {"variable": ["A", "B", "C"]}
    arr = ds.to_array().assign_coords(var_coords)

    colormap = mpl.colormaps[colormap_name]
    min_, max_ = arr.min().data, arr.max().data
    norm = SymLogNorm(linthresh=3, linscale=1, vmin=min_, vmax=max_ * 2, base=2)

    return ColorNorm(colormap, norm)


def create_pressue_geometry_plot(
    comparison: ComparisonData,
    geom_cnorm: ColorNorm,
    flow_cnorm: ColorNorm,
    fig: Figure,
    ax: Axes,
    hour=12,
):
    path = comparison.path
    case = get_ezcase_for_path(path)
    pressure = get_qoi("AFN Node Total Pressure", path)
    data_at_noon = pressure.select_time(hour)
    # print(data_at_noon)

    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", path)
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", path)
    net_flow = flow_12.select_time(hour) - flow_21.select_time(hour)
    # print(net_flow)

    dp = DataPlot(case.objects.zones, cardinal_expansion_factor=2)
    dp.fig = fig
    dp.axes = ax

    dp.plot_zone_names()
    dp.plot_zones_with_data(data_at_noon, *geom_cnorm)
    dp.plot_cardinal_names_with_data(data_at_noon, *geom_cnorm)
    dp.plot_subsurfaces_and_surfaces(
        case.objects.airflow_network,
        case.objects.airboundaries,
        case.objects.subsurfaces,
    )
    dp.plot_connections_with_data(
        net_flow, case.objects.airflow_network.afn_surfaces, *flow_cnorm
    )
    dp.set_limits()
    return dp


def create_geometry_plots():
    comp_data = assemble_default_data("20251105_door_sched")
    # print([i.case for i in comp_data.values])
    exp0, exp1, exp2 = comp_data
    geom_cnorm = create_pressure_cnorm()
    flow_cnorm = create_flow_cnorm()

    fig, axs = plt.subplots(ncols=3, figsize=(24, 10))
    for exp, ax in zip(comp_data, axs):
        print(f"case: {exp.case_name}")
        dp = create_pressue_geometry_plot(exp, geom_cnorm, flow_cnorm, fig, ax)

    geom_bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=geom_cnorm.norm, cmap=geom_cnorm.cmap),
            orientation="vertical",
            label="Total Pressure [Pa]",
            ax=axs[2],
            shrink=0.5,
        ),
    )
    flow_bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=flow_cnorm.norm, cmap=flow_cnorm.cmap),
            orientation="vertical",
            label="Total Pressure [Pa]",
            ax=axs[2],
            shrink=0.5,
        ),
    )
    plt.show()


if __name__ == "__main__":
    create_geometry_plots()
    # res = study_pressure_data()
