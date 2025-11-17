from p1gen._03_execute.assemble import assemble_default_data
from astropy.visualization import ImageNormalize, ZScaleInterval
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from replan2eplus.results.sql import get_qoi
from p1gen.paths import CampaignNameOptions
import matplotlib.cm as cm
from p1gen.plot_utils.utils import NamedData
from p1gen.config import CURRENT_CAMPAIGN
from p1gen.plot_utils.utils import filter_to_time
from matplotlib.axes import Axes
import matplotlib as mpl


def process_data_arr(arr: xr.DataArray):
    narr = arr.dropna(dim="space_names").drop_vars("space_names")

    new_coords = {"space_names": range(narr.size)}
    narr2 = narr.assign_coords(new_coords)
    return narr2.sortby(narr2)


def study_pressure_data(
    hour: int = 12, campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN
):

    comp_data = assemble_default_data(campaign_name)
    pressures = [
        NamedData(
            i.case_name,
            filter_to_time(
                get_qoi("AFN Node Total Pressure", i.path).data_arr, hour=hour
            ),
        )
        for i in comp_data
    ]
    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in pressures})
    ds_mix = xr.Dataset(
        data_vars={i.case_name: process_data_arr(i.data_arr) for i in pressures}
    )

    return ds, ds_mix


def create_basic(Z: np.ndarray, ax: Axes, colormap: Colormap, fig):
    pc = ax.pcolormesh(Z, cmap=colormap)
    fig.colorbar(pc, shrink=0.5)
    ax.set_title("Original")


def create_modified(arr: xr.DataArray, Z: np.ndarray, ax: Axes, colormap: Colormap):
    min_, max_ = arr.min().data, arr.max().data
    norm = ImageNormalize(Z, interval=ZScaleInterval())

    plt.colorbar(
        cm.ScalarMappable(norm=norm, cmap=colormap),
        orientation="vertical",
        label="Total Pressure [Pa]",
        ax=ax,
    )
    ax.pcolormesh(Z, cmap=colormap, norm=norm)
    ax.set_title("modification")
    return ax


def plot_to_study_colormap(ds: xr.Dataset):
    var_coords = {"variable": ["A", "B", "C"]}
    arr = ds.to_array().assign_coords(var_coords)

    Z = arr.data
    colormap = mpl.colormaps["RdYlBu_r"]
    # colormap = cmr.guppy  # plt.get_cmap("cmr.prinsenvlag")I

    fig, (ax1, ax2) = plt.subplots(ncols=2)
    ax1 = create_basic(Z, ax1, colormap, fig)
    ax2 = create_modified(arr, Z, ax2, colormap)


if __name__ == "__main__":
    dsi, ds = study_pressure_data()
    img = plot_to_study_colormap(ds)
    plt.show()
