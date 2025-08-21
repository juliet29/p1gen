from dataclasses import dataclass
from typing import Literal

from geomeppy import IDF
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.visuals.calcs import domain_to_line
from utils4plans.lists import chain_flatten

from p1gen.paths import test_case
from p1gen.utils import read_idf
from p1gen.utils import CurrCase

OPENING = "AIRFLOWNETWORK:MULTIZONE:COMPONENT:SIMPLEOPENING"
DOOR = "Door"
WINDOW = "Window"

Color = Literal["navy", "deepskyblue", "gray", "snow", "saddlebrown", "white", "black"]
LineStyle = Literal[
    "-",
    "--",
    "-.",
    ":",
]


def prep_plot_surface_2d(
    items: list[Surface] | list[Subsurface],
    color: Color,
    label="",
    linestyle: LineStyle = "-",
    linweidth=1,
    gapcolor:Color="white",
):
    line2Ds = []
    for ix, item in enumerate(items):
        line = domain_to_line(item.domain)
        line2D = line.to_line2D
        line2D.set_color(color)
        line2D.set_linestyle(linestyle)
        line2D.set_linewidth(linweidth)
        line2D.set_gapcolor(gapcolor)
        line2Ds.append(line2D)
        if ix == 0:
            line2D.set_label(label)

    return line2Ds


@dataclass
class SurfacePlots:
    afn_surfaces: list[Subsurface]
    non_afn_surfaces: list[Subsurface]  # grey solid
    doors: list[Subsurface]  # brown
    windows: list[Subsurface]  # dark blue
    air_boundaries: list[Surface]  # white dashed

    @property
    def prep_non_afn_surfaces(self):
        return prep_plot_surface_2d(
            self.non_afn_surfaces, "gray", "Not in Airflow Network", linestyle="-"
        )

    @property
    def prep_doors(self):
        return prep_plot_surface_2d(self.doors, "saddlebrown", "Door")

    @property
    def prep_windows(self):
        return prep_plot_surface_2d(self.windows, "deepskyblue", "Window")

    @property
    def prep_airboundaries(self):
        return prep_plot_surface_2d(
            self.air_boundaries, "snow", "AirBoundary", ":", linweidth=1, gapcolor="gray"
        )

    @property
    def all_lines(self):
        return chain_flatten(
            [
                self.prep_non_afn_surfaces,
                self.prep_windows,
                self.prep_doors,
                self.prep_airboundaries,
            ]
        )


def get_afn_opening_names(idf: IDF):
    def edit_name(s: str):
        return " ".join(s.split(" ")[0:-1])

    openings = idf.idfobjects[OPENING]

    return [edit_name(i.Name) for i in openings]


def organize_subsurfaces(
    subsurfaces: list[Subsurface], surfaces: list[Surface], afn_opening_names: list[str]
):
    afn_subsurfaces = [i for i in subsurfaces if i.subsurface_name in afn_opening_names]
    non_afn_subsurfaces = [i for i in subsurfaces if i not in afn_subsurfaces]
    doors = [i for i in afn_subsurfaces if DOOR in i.subsurface_name]
    windows = [i for i in afn_subsurfaces if WINDOW in i.subsurface_name]

    afn_walls = [
        i for i in surfaces if i._idf_name in afn_opening_names
    ]  # == air boundary walls

    return SurfacePlots(afn_subsurfaces, non_afn_subsurfaces, doors, windows, afn_walls)


def create_geom_plot(case: CurrCase):
    assert case.idf
    afn_openings = get_afn_opening_names(case.idf.idf)
    surface_lines = organize_subsurfaces(case.subsurfaces, case.surfaces, afn_openings)

    bp = (
        BasePlot(case.zones, cardinal_expansion_factor=1.8)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal()
        # .plot_subsurfaces(case.subsurfaces)
        .plot_connections(surface_lines.afn_surfaces)
    )

    for line in surface_lines.all_lines:
        bp.axes.add_artist(line)

    bp.axes.legend()
    bp.show()


if __name__ == "__main__":
    case = read_idf(test_case)
    create_geom_plot(case)

    pass
