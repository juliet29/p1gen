from p1gen._03_execute.assemble import assemble_default_data

import xarray as xr
from replan2eplus.results.sql import get_qoi
from p1gen.paths import CampaignNameOptions
from p1gen.config import CURRENT_CAMPAIGN
from typing import NamedTuple


class SiteVariables(NamedTuple):
    temp: xr.DataArray
    wind_dir: xr.DataArray


def get_site_data(campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN):
    exp = assemble_default_data(campaign_name)[0]
    temp = get_qoi("Site Outdoor Air Drybulb Temperature", exp.path).data_arr
    wind_dir = get_qoi("Site Wind Direction", exp.path).data_arr
    wind_speed = get_qoi("Site Wind Speed", exp.path).data_arr

    names = ["temperature", "wind_dir", "wind_speed"]

    ds = xr.Dataset({name: da for name, da in zip(names, [temp, wind_dir, wind_speed])})

    return ds
