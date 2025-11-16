from pathlib import Path
from p1gen.plot_utils.utils import filter_to_time
import numpy as np
from typing import NamedTuple

import matplotlib as mpl
from matplotlib.axes import Axes
import matplotlib.cm as cm
from matplotlib.colors import Colormap, Normalize, BoundaryNorm
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from replan2eplus.results.sql import get_qoi
from replan2eplus.visuals.data.many_data_plot import DataPlot
import xarray as xr

from p1gen._03_execute.assemble import ComparisonData, assemble_default_data
from p1gen.paths import get_ezcase_for_path, CampaignNameOptions
from p1gen.config import CURRENT_CAMPAIGN, DEBUG_FIGURES
from p1gen.plot_utils.utils import NamedData
from p1gen.plot_utils.save import save_figure


class ColorNorm(NamedTuple):
    cmap: Colormap
    norm: Normalize


def get_pressure_for_path(path: Path, hour: int = 12):
    pressure = get_qoi("AFN Node Total Pressure", path)
    data_at_hour = filter_to_time(pressure.data_arr, hour=hour)
    return data_at_hour


def get_flow_for_path(path: Path, hour: int = 12):
    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", path).data_arr
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", path).data_arr
    f12t, f21t = filter_to_time(flow_12, hour=hour), filter_to_time(flow_21, hour=hour)
    net_flow = f12t - f21t
    return net_flow


def create_pressure_cnorm(hour=12):
    comp_data = assemble_default_data("20251105_door_sched")
    pressures = [
        NamedData(i.case_name, get_pressure_for_path(i.path, hour)) for i in comp_data
    ]

    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in pressures})
    arr = ds.to_array()
    var_coords = {"variable": ["A", "B", "C"]}
    arr = ds.to_array().assign_coords(var_coords)

    colormap = mpl.colormaps["RdYlBu_r"]
    min_, max_ = arr.min().data, arr.max().data

    rg = np.arange(-5, -1, 0.1)
    rg_pos = np.linspace(3, 5, len(rg))
    rg.tolist()
    levels = rg.tolist() + [0] + rg_pos.tolist()
    norm = BoundaryNorm(boundaries=levels, ncolors=256)

    return ColorNorm(colormap, norm)


def create_flow_cnorm(hour=12, colormap_name: str = "PuBu"):
    comp_data = assemble_default_data("20251105_door_sched")

    flow_data = [
        NamedData(i.case_name, get_flow_for_path(i.path, hour=hour)) for i in comp_data
    ]

    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in flow_data})
    var_coords = {"variable": ["A", "B", "C"]}
    arr = abs(ds.to_array()).assign_coords(var_coords)

    colormap = mpl.colormaps[colormap_name]
    min_, max_ = arr.min().data, arr.max().data
    norm = Normalize(vmin=min_, vmax=max_)

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
    net_flow = get_flow_for_path(path, hour)
    pressure = get_pressure_for_path(path, hour)

    dp = DataPlot(case.objects.zones, cardinal_expansion_factor=1.3)
    dp.fig = fig
    dp.axes = ax

    dp.plot_zone_names()
    dp.plot_zones_with_data(pressure, *geom_cnorm)
    dp.plot_cardinal_names_with_data(pressure, *geom_cnorm)
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


@save_figure(CURRENT_CAMPAIGN, "pressure_geom", DEBUG_FIGURES)
def create_geometry_plots(
    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN, hour: int = 12
):
    comp_data = assemble_default_data(campaign_name)
    geom_cnorm = create_pressure_cnorm(hour)
    flow_cnorm = create_flow_cnorm(hour)

    fig, axs = plt.subplots(ncols=3, figsize=(24, 10))
    for exp, ax in zip(comp_data, axs):
        print(f"case: {exp.case_name}")
        create_pressue_geometry_plot(exp, geom_cnorm, flow_cnorm, fig, ax, hour)
        # ax.set_xlim(-1, 10)
        # ax.set_ylim(-1, 12)
        # ax.spines["top"].set_visible(False)
        # ax.spines["right"].set_visible(False)

    geom_bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=geom_cnorm.norm, cmap=geom_cnorm.cmap),
            orientation="horizontal",
            label="Total Pressure [Pa]",
            ax=axs,
            shrink=0.5,
        ),
    )
    flow_bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=flow_cnorm.norm, cmap=flow_cnorm.cmap),
            orientation="horizontal",
            label="Net Ventilation Flow Rate [m3/s]",
            ax=axs,
            shrink=0.5,
        ),
    )
    # plt.show()
    return fig


if __name__ == "__main__":
    create_geometry_plots()
    # res = study_pressure_data()
