from pathlib import Path
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.ezobjects.subsurface import Subsurface

from p1gen.paths import IDF_NAME, PATH_TO_IDD


def get_zone_by_name(name: str, zones: list[Zone]):
    possible = [i for i in zones if i.zone_name == name]
    if len(possible) == 0:
        possible = [i for i in zones if i.zone_name.upper() == name]
    if len(possible) == 0:
        return None
    return possible[0]


def get_surface_by_name(name: str, surfaces: list[Surface]):
    possible = [i for i in surfaces if i.surface_name == name]
    if len(possible) == 0:
        possible = [i for i in surfaces if i.surface_name.upper() == name]
    if len(possible) == 0:
        return None
    return possible[0]

def get_subsurface_by_name(name: str, subsurfaces: list[Subsurface]):
    possible = [i for i in subsurfaces if i.subsurface_name == name]
    if len(possible) == 0:
        possible = [i for i in subsurfaces if i.subsurface_name.upper() == name]
    if len(possible) == 0:
        return None
    return possible[0]

def get_surface_or_subsuface_by_name(name: str, objects: list[Subsurface | Surface]):
    surfaces = [i for i in objects if isinstance(i, Surface)]
    subsurfaces = [i for i in objects if isinstance(i, Subsurface)]
    res = get_surface_by_name(name, surfaces)
    if not res:
        res = get_subsurface_by_name(name, subsurfaces)
    if not res:
        return None 
    return res



class CurrCase(ExistCase):
    case_name: str = ""
    @property
    def zone_names(self):
        return  [i.zone_name.upper() for i in self.zones]
    
    @property
    def subsurface_names(self):
        return [i.subsurface_name.upper() for i in self.subsurfaces]
    
    @property
    def geom_names(self):
        surfaces = [i.surface_name for i in self.surfaces]
        return [i.upper() for i in self.zone_names + surfaces +  self.subsurface_names]


def read_idf(path_to_case: Path):
    case = CurrCase(PATH_TO_IDD, path_to_case / IDF_NAME)
    case.initialize_idf()
    case.get_objects()
    return case  # , zones


# get
