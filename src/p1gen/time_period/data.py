from p1gen._03_execute.zone_size import get_afn_zone_names
from p1gen._03_execute.assemble import ComparisonData, assemble_default_data
import xarray as xr
from replan2eplus.results.sql import get_qoi
from p1gen.paths import CampaignNameOptions
from p1gen.config import CURRENT_CAMPAIGN
from p1gen.plot_utils.utils import NamedData


def find_max_dif_external_nodes(arr_: xr.DataArray):
    arr = arr_.loc[:, arr_.space_names.str.contains("external_node".upper())]
    assert arr.space_names.size > 2
    return arr.max(dim="space_names") - arr.min(dim="space_names")


def find_max_dif_internal_nodes(arr_: xr.DataArray):
    arr = arr_.loc[:, arr_.space_names.str.contains("block".upper())]
    assert arr.space_names.size > 2
    return arr.max(dim="space_names") - arr.min(dim="space_names")


def get_data_for_pressure(
    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN,
):
    experiments = assemble_default_data(campaign_name)
    pressure_data = [
        NamedData(i.case_name, get_qoi("AFN Node Total Pressure", i.path).data_arr)
        for i in experiments
    ]
    max_dif_internal = xr.Dataset(
        data_vars={
            i.case_name: find_max_dif_internal_nodes(i.data_arr) for i in pressure_data
        }
    )

    max_dif_external = xr.Dataset(
        data_vars={
            i.case_name: find_max_dif_external_nodes(i.data_arr) for i in pressure_data
        }
    )

    return max_dif_internal, max_dif_external


def get_data_for_flow(
    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN,
):
    experiments = assemble_default_data(campaign_name)

    def make_data_array(exp: ComparisonData):
        flow12 = get_qoi(
            "AFN Linkage Node 1 to Node 2 Volume Flow Rate", exp.path
        ).data_arr
        flow21 = get_qoi(
            "AFN Linkage Node 2 to Node 1 Volume Flow Rate", exp.path
        ).data_arr
        data = (abs(flow12 - flow21)).mean(dim="space_names")
        return NamedData(exp.case_name, data)

    flow_data = [make_data_array(i) for i in experiments]

    flow_ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in flow_data})
    return flow_ds


def get_data_for_temperature_simple(
    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN,
):
    experiments = assemble_default_data(campaign_name)

    def make_data_array(exp: ComparisonData):
        temp_data = get_qoi("Zone Mean Air Temperature", exp.path).data_arr
        afn_zone_names = get_afn_zone_names(exp.path)
        afn_filter = temp_data.space_names.isin(afn_zone_names)
        afn_data = temp_data.sel(space_names=afn_filter).mean(dim="space_names")
        return NamedData(exp.case_name, afn_data)

    temp_data = [make_data_array(i) for i in experiments]

    tds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in temp_data})
    return tds


def get_data_for_temperature_deviation(
    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN,
):
    experiments = assemble_default_data(campaign_name)
    site_temp = get_qoi(
        "Site Outdoor Air Drybulb Temperature", experiments[0].path
    ).data_arr.squeeze()

    def make_data_array(exp: ComparisonData):
        temp_data = get_qoi("Zone Mean Air Temperature", exp.path).data_arr
        afn_zone_names = get_afn_zone_names(exp.path)
        afn_filter = temp_data.space_names.isin(afn_zone_names)
        afn_data = temp_data.sel(space_names=afn_filter).mean(dim="space_names")
        return NamedData(exp.case_name, afn_data - site_temp)

    temp_data = [make_data_array(i) for i in experiments]

    tds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in temp_data})

    return tds


def get_data_for_ach(
    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN,
):
    experiments = assemble_default_data(campaign_name)

    def make_data_array(exp: ComparisonData):
        data = get_qoi("AFN Zone Ventilation Air Change Rate", exp.path).data_arr
        da = data.where(data > 0, drop=True).mean(dim="space_names")
        return NamedData(exp.case_name, da)

    ach_data = [make_data_array(i) for i in experiments]
    ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in ach_data})
    return ds  # ach_data  # ds


#
#
# def plot_histogram_of_ach_data_arr(ds: list[NamedData]):
#     fig, axs = plt.subplots(ncols=3)
#     names = ds
#     for ix, name in enumerate(names):
#         name.data_arr.plot.hist(
#             ax=axs[ix], density=True, histtype="step", cumulative=True
#         )
#
#     plt.show()
#
#
# def plot_histogram_of_ach(ds: xr.Dataset):
#     fig, axs = plt.subplots(ncols=3)
#     names = ["A", "B", "C"]
#     for ix, name in enumerate(names):
#         ds[name].plot.hist(
#             ax=axs[ix],
#             density=True,
#             histtype="step",
#             cumulative=True,
#         )
#
#     plt.show()
#

experiments = assemble_default_data("20251105_door_sched")
exp = experiments[0]
temp_data2 = get_qoi("Zone Mean Air Temperature", exp.path).data_arr


if __name__ == "__main__":
    pass
    # ds = get_data_for_ach("20251112_summer_update_dv")
    # plot_histogram_of_ach_data_arr(ds)
    # night_ds, day_ds = get_data_for_temperature()
    # print(tds[0])
