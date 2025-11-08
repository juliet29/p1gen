from replan2eplus.ezcase.ez import EZ
from pathlib import Path
from rich import print
from p1gen._03_execute.assemble import assemble_default_data
from p1gen.paths import Constants
from typing import NamedTuple
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.ortho_domain import OrthoDomain


class ZoneValues(NamedTuple):
    name: str
    value: float


class ZoneSizesList(NamedTuple):
    values: list[ZoneValues]

    @property
    def total(self):
        return sum([i.value for i in self.values])

    @property
    def percents(self):
        return [ZoneValues(i.name, i.value / self.total) for i in self.values]


def get_zone_areas(path: Path):
    case = EZ(path / Constants.IDF_NAME)
    zones = case.objects.zones
    res = []
    for zone in zones:
        if isinstance(zone.domain, OrthoDomain):
            raise NotImplementedError("Havent done areas for ortho domains!")
        res.append(ZoneValues(zone.zone_name, zone.domain.area))

    return ZoneSizesList(res)


def get_afn_zone_names(path: Path):
    case = EZ(path / Constants.IDF_NAME)
    afn_zones = case.objects.airflow_network.zones
    afn_zone_names = [i.zone_name.upper() for i in afn_zones]
    return afn_zone_names


if __name__ == "__main__":
    exp = assemble_default_data("20251105_door_sched")[0]
    # get_zone_areas(exp.path)
    get_afn_zone_names(exp.path)
