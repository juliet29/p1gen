from p1gen.plot_utils.utils import group_dataset_by_time
import xarray as xr
from typing import NamedTuple

from p1gen.time_period.data import (
    get_data_for_ach,
    get_data_for_flow,
    get_data_for_pressure,
    get_data_for_temperature,
    get_data_for_temperature_simple,
)


class DayNightData(NamedTuple):
    day: xr.Dataset
    night: xr.Dataset


class QOIData(NamedTuple):
    max_diff_int_pressure: DayNightData
    max_diff_ext_pressure: DayNightData
    flow: DayNightData
    temp: DayNightData
    temp_dev: DayNightData
    ach: DayNightData


def get_day_night_data():
    max_diff_int_pressure, max_diff_ext_pressure = get_data_for_pressure()
    flow = get_data_for_flow()
    temp = get_data_for_temperature_simple()
    temp_dev = get_data_for_temperature()
    ach = get_data_for_ach()

    datas = [max_diff_int_pressure, max_diff_ext_pressure, flow, temp, temp_dev, ach]
    split_data = [DayNightData(*group_dataset_by_time(i)) for i in datas]
    return QOIData(*split_data)


if __name__ == "__main__":
    get_day_night_data()
