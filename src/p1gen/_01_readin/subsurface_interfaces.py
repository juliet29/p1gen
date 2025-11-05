from typing import Literal

from pydantic import BaseModel, ConfigDict
from replan2eplus.ops.subsurfaces.ezobject import Edge as ReplanEdge
from replan2eplus.ops.subsurfaces.interfaces import Dimension, Location
from replan2eplus.ops.subsurfaces.user_interfaces import Detail, EdgeGroup
from utils4plans.sets import set_difference


class WindowDetail(BaseModel):
    id: int
    width: float
    height: float
    # head_height: float # TODO incorporate this into how read susburfaces..

    @property
    def true_detail(self):
        return Detail(
            dimension=Dimension(self.width, self.height),
            location=Location("mm", "CENTROID", "CENTROID"),
            type_="Window",
        )


class DoorDetail(BaseModel):
    id: int
    width: float
    height: float
    thickness: float
    # TODO have some validation about thickness.. -> material width should have this

    @property
    def true_detail(self):
        return Detail(
            dimension=Dimension(self.width, self.height),
            location=Location("bm", "SOUTH", "SOUTH"),
            type_="Door",
        )




class DesignDetails(BaseModel):
    WINDOWS: list[WindowDetail]
    DOORS: list[DoorDetail]

    @property
    def windows_dict(self) -> dict[str, Detail]:
        return {f"Window_{i.id}": i.true_detail for ix, i in enumerate(self.WINDOWS)}

    @property
    def doors_dict(self) -> dict[str, Detail]:
        return {f"Door_{i.id}": i.true_detail for ix, i in enumerate(self.DOORS)}

    @property
    def details_dict(self):
        return self.windows_dict | self.doors_dict



    @property
    def door_ix_bump(self):
        return len(self.WINDOWS)


class DetailsForLinks(BaseModel):
    model_config = ConfigDict(frozen=True)
    external: bool
    id: int


class Edge(BaseModel):
    model_config = ConfigDict(frozen=True)

    details: DetailsForLinks  # Tyoped dict
    source: str
    target: str  # TODO -> can we validate against existing rooms? # maybe have separate function, and this happens in replan2eplus..

    @property
    def replan_edge(self):
        return ReplanEdge(space_a=self.source, space_b=self.target)


class EdgesList(BaseModel):
    links: list[Edge]  # TODO include possible alias
    """
    mini read me for details:
    0 - airboundary 
    internal - doors
    external - windows
    
    """

    @property
    def airboundary_links(self):
        return list(
            filter(
                lambda x: not x.details.external and x.details.id == 0, self.links
            )  # TODO put the details config in a readme or in an actual config file that can be read by both..
        )

    @property
    def airboundary_edges(self):
        return [i.replan_edge for i in self.airboundary_links]

    @property
    def true_subsurfaces(self):
        return set_difference(self.links, self.airboundary_links)

    @property
    def internal_edges(self):
        return [i.replan_edge for i in self.true_subsurfaces if not i.details.external]

    @property
    def external_edges(self):
        return [i.replan_edge for i in self.true_subsurfaces if i.details.external]

    def create_edge_group(
        self,
        replan_edges: list[ReplanEdge],
        detail_name: str,
        type_: Literal["Zone_Direction", "Zone_Zone"],
    ):
        return EdgeGroup(replan_edges, detail_name, type_)
