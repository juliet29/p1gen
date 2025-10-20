from pydantic import BaseModel, ConfigDict
from replan2eplus.ezobjects.subsurface import Edge as ReplanEdge
from replan2eplus.ops.subsurfaces.interfaces import Detail, Dimension, Location
from bidict import bidict

from typing import Literal, NamedTuple
from collections import Counter
from replan2eplus.ezobjects.subsurface import Edge as ReplanEdge
from utils4plans.sets import set_difference
from replan2eplus.ops.subsurfaces.interfaces import EdgeGroup


# TODO maybe these inherit from something that can convert to the subsurface loc type..


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


class SubsurfacePair(NamedTuple):
    type_: Literal["DOOR", "WINDOW"]
    id: int


class DesignDetails(BaseModel):
    WINDOWS: list[WindowDetail]
    DOORS: list[DoorDetail]

    # TODO when creating these, doors and windows should each have unique ids..
    # here doing a work around where going to reassign these.. ids..
    # @property
    # def windows_map(self):
    #     return {i.id: i for i in self.WINDOWS}

    # @property
    # def doors_map(self):
    #     return {i.id: i for i in self.DOORS}

    # @property
    # def group_map(self):
    #     counter = 0
    #     group_dict: dict[int, SubsurfacePair] = {}
    #     for item in self.WINDOWS:
    #         group_dict[counter] = SubsurfacePair("WINDOW", item.id)
    #         counter += 1

    #     for item in self.DOORS:
    #         group_dict[counter] = SubsurfacePair("DOOR", item.id)
    #         counter += 1
    #     return bidict(group_dict)

    # @property
    # def details_map(self):
    #     def get_detail(v: SubsurfacePair):
    #         if v.type_ == "WINDOW":
    #             return self.windows_map[v.id].true_detail
    #         else:
    #             return self.doors_map[v.id].true_detail
    #         # TODO what if is neither?

    #     return {k: get_detail(v) for k, v in self.group_map.items()}

    # @property
    # def map_(self):
    #     return {ix: i.true_detail for ix, i in enumerate(self.WINDOWS + self.DOORS)}

    # TODO second map with the correct details..

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

    # as air boundaries..
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
        return [i.replan_edge for i in self.true_subsurfaces if not i.details.external]

    def create_edge_group(
        self,
        replan_edges: list[ReplanEdge],
        detail_name: str,
        type_: Literal["Zone_Direction", "Zone_Zone"],
    ):
        return EdgeGroup(replan_edges, detail_name, type_)

    # @property
    # def true_subsurfaces_dict(self):
    #     return bidict({ix: i for ix, i in enumerate(self.true_subsurfaces)})

    # @property
    # def true_subsurfaces_dict_as_edges(self):
    #     return {ix: i.as_replan_edge for ix, i in enumerate(self.true_subsurfaces)}

    # @property
    # def windows_map(self):
    #     return sort_and_group_objects_dict(
    #         [i for i in self.true_subsurfaces if i.details.external],
    #         lambda x: x.details.id,
    #     )

    #     # now have to match to the group map..

    # @property
    # def doors_map(self):
    #     return sort_and_group_objects_dict(
    #         [i for i in self.true_subsurfaces if not i.details.external],
    #         lambda x: x.details.id,
    #     )

    # def make_updated_map(self, design_details: DesignDetails):
    #     new_map: dict[int, list[int]] = {}

    #     def update_map(adict: dict[int, list[Edge]], type_: Literal["DOOR", "WINDOW"]):
    #         for k, list_of_edges in adict.items():
    #             details_ix = design_details.group_map.inverse[SubsurfacePair(type_, k)]
    #             edge_ids = [
    #                 self.true_subsurfaces_dict.inverse[i] for i in list_of_edges
    #             ]
    #             new_map[details_ix] = edge_ids
    #         return new_map

    #     new_map = update_map(self.doors_map, "DOOR")
    #     new_map = update_map(self.windows_map, "WINDOW")
    #     return new_map
