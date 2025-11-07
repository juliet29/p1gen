from p1gen._03_execute import zone_size
from p1gen._03_execute.assemble import assemble_default_data
from typing import NamedTuple
import xarray as xr
from replan2eplus.results.sql import get_qoi
from datetime import time, date
from replan2eplus.ops.schedules.interfaces.constants import DAY_START_TIME, DAY_END_TIME
from p1gen.paths import CampaignNameOptions
from replan2eplus.ops.schedules.interfaces.utils import create_datetime


def find_max_dif_external_nodes(arr_: xr.DataArray):
    arr = arr_.loc[:, arr_.space_names.str.contains("external_node".upper())]
    assert arr.space_names.size > 2
    return arr.max(dim="space_names") - arr.min(dim="space_names")


def find_max_dif_internal_nodes(arr_: xr.DataArray):
    arr = arr_.loc[:, arr_.space_names.str.contains("block".upper())]
    # print(arr) # TODO better if uses NOT external node
    assert arr.space_names.size > 2
    return arr.max(dim="space_names") - arr.min(dim="space_names")


class NamedData(NamedTuple):
    case_name: str
    data_arr: xr.DataArray


def get_data_for_pressure(
    campaign_name: CampaignNameOptions = "20251105_door_sched",
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
    # now, want to assemble this into one data array
    # isolate the external nodes -> assert that there is > 2
    # find the min and max at each time, and take their difference..


quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]


morning_end = time(6)
day_end = time(18)


def daymap(ts: list[time]):
    return list(map(lambda x: create_datetime(x, date_=date(2025, 7, 1)), ts))


early_morning = slice(DAY_START_TIME, morning_end)
daytime = slice(morning_end, day_end)
night = slice(day_end, DAY_END_TIME)


def find_max_flow(arr: xr.DataArray):
    arr.median(dim="space_names").quantile(q=quantiles)
    pass


def get_data_for_flow(
    campaign_name: CampaignNameOptions = "20251105_door_sched",
):
    experiments = assemble_default_data(campaign_name)
    # TODO make this more readable!
    flow_data = [
        NamedData(
            i.case_name,
            abs(
                get_qoi(
                    "AFN Linkage Node 1 to Node 2 Volume Flow Rate", i.path
                ).data_arr
                - get_qoi(
                    "AFN Linkage Node 2 to Node 1 Volume Flow Rate", i.path
                ).data_arr
            ),
        )
        for i in experiments
    ]

    flow_ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in flow_data})
    return flow_ds


def get_data_for_temperature(
    campaign_name: CampaignNameOptions = "20251105_door_sched",
):
    experiments = assemble_default_data(campaign_name)
    site_temp = get_qoi(
        "Site Outdoor Air Drybulb Temperature", experiments[0].path
    ).data_arr.squeeze()
    temp_data = [
        NamedData(
            i.case_name,
            get_qoi("Zone Mean Air Temperature", i.path).data_arr.mean(
                dim="space_names"
            )
            - site_temp,
        )
        for i in experiments
    ]  # TODO write a check for this.. pos value should mean zone is wamer than outside..

    exp = experiments[0]
    temp_data2 = get_qoi("Zone Mean Air Temperature", exp.path).data_arr
    zone_sizes = zone_size.get_zone_areas(exp.path)

    temp_ds = xr.Dataset(data_vars={i.case_name: i.data_arr for i in temp_data})

    zone_size_arr = xr.DataArray(
        data=[i.value for i in zone_sizes.percents],
        coords={"space_names": [i.name.upper() for i in zone_sizes.values]},
    )

    weighted_temp_ds = zone_size_arr * temp_ds

    return temp_ds, temp_data2, zone_size_arr


def plot_pressure_dif():
    pass


if __name__ == "__main__":
    tds, temp_data2, zone_sizes = get_data_for_temperature()
    # print(tds[0])
