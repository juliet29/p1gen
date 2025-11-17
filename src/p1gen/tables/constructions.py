from typing import Iterable, NamedTuple
from rich import print
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.constructions.idfobject import IDFConstruction
from geomeppy import IDF

from p1gen._03_execute.assemble import ComparisonData, assemble_default_data
from p1gen.config import CURRENT_CAMPAIGN
from p1gen.paths import CampaignNameOptions, get_ezcase_for_path


def get_construction_for_group(
    idf: IDF,
    group: Iterable[Surface | Subsurface],
):
    sample = list(group)[0]
    const_name = sample.construction_name
    print(f"{const_name=}")
    # res = IDFConstruction.read_by_name(idf, [const_name])
    res2 = IDFConstruction().get_one_idf_object(idf, const_name)

    # print(res2.rvalue_ip)
    return res2


class ConstructionData(NamedTuple):
    idf: IDF
    surfaces: list[Surface]
    subsurfaces: list[Subsurface]

    @property
    def interior_wall(self):
        res = filter(lambda x: x.boundary_condition == "surface", self.surfaces)
        return get_construction_for_group(self.idf, res)


def get_basic_data(campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN):
    def get(exp: ComparisonData):
        case = get_ezcase_for_path(exp.path)
        objs = get_ezcase_for_path(exp.path).objects

        return ConstructionData(case.idf, objs.surfaces, objs.subsurfaces)

    comparison_data = assemble_default_data(campaign_name)[0:1]
    return [get(i) for i in comparison_data]


if __name__ == "__main__":
    da = get_basic_data()[0]
    res = da.interior_wall
    print(res)
