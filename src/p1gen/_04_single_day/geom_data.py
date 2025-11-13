from p1gen._03_execute.assemble import assemble_default_data
from matplotlib.colors import BoundaryNorm
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr
from datetime import datetime
from replan2eplus.results.sql import get_qoi
from p1gen.paths import CampaignNameOptions
import matplotlib.cm as cm
from p1gen.plot_utils.utils import NamedData


STUDY_DATE = (2017, 7, 1)


def filter_to_time(
    arr: xr.DataArray, date_: tuple[int, int, int] = STUDY_DATE, hour: int = 12
):
    return arr.sel(datetimes=datetime(*date_, hour=hour, minute=0))


def process_data_arr(arr: xr.DataArray):
    narr = arr.dropna(dim="space_names").drop_vars("space_names")

    new_coords = {"space_names": range(narr.size)}
    narr2 = narr.assign_coords(new_coords)
    return narr2.sortby(narr2)


def study_pressure_data(
    hour: int = 12, campaign_name: CampaignNameOptions = "20251109_summer"
):

    comp_data = assemble_default_data(campaign_name)
    pressures = [
        NamedData(
            i.case_name,
            filter_to_time(get_qoi("AFN Node Total Pressure", i.path).data_arr),
        )
        for i in comp_data
    ]
    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in pressures})
    ds_mix = xr.Dataset(
        data_vars={i.case_name: process_data_arr(i.data_arr) for i in pressures}
    )

    return ds, ds_mix


# def plot_histogram_at_time(ds: xr.Dataset):
#     fig, ax = plt.subplots()jk
#     res = ds.to_array().plot.hist(ax=ax)
#     plt.show()


def plot_to_study_colormap(ds: xr.Dataset):
    var_coords = {"variable": ["A", "B", "C"]}
    arr = ds.to_array().assign_coords(var_coords)

    X, Y = np.meshgrid(arr.variable, arr.space_names)
    Z = arr.data

    colormap = mpl.colormaps["RdYlBu_r"]

    fig, (ax1, ax2) = plt.subplots(ncols=2)

    # axis 1
    pc = ax1.pcolormesh(Z, cmap=colormap)
    fig.colorbar(pc, shrink=0.5)
    ax1.set_title("Original")

    # axis 2
    min_, max_ = arr.min().data, arr.max().data

    rg = np.arange(-4, -1, 0.1)
    rg_pos = np.arange(1, 4, 0.1)
    rg.tolist()
    levels = [-5] + rg.tolist() + [0] + rg_pos.tolist() + [5]
    norm = BoundaryNorm(boundaries=levels, ncolors=256)

    plt.colorbar(
        cm.ScalarMappable(norm=norm, cmap=colormap),
        orientation="vertical",
        label="Total Pressure [Pa]",
        ax=ax2,
    )
    pc = ax2.pcolormesh(Z, cmap=colormap, norm=norm)
    ax2.set_title("modification")
    # not straightforward to access mpl normalization functionality
    # res = arr.plot()
    return pc


if __name__ == "__main__":
    dsi, ds = study_pressure_data()
    img = plot_to_study_colormap(ds)
    plt.show()
