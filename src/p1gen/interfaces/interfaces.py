# plan.json layout
from pydantic import BaseModel, Field

# TODO these need to be brought up to init -> EZcase and the things for defining it
from replan2eplus.zones.interfaces import Room
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range


HEIGHT = 3.05  # TODO read from config!


class RoomInPlan(BaseModel):
    id: int
    label: str
    left: float  # PyDantic handles converting float like to float!
    top: float
    width: float
    height: float
    color: str = Field(default="")

    @property
    def as_replan2eplus_room(self):
        horz_range = Range(self.left, self.left + self.width)
        vert_range = Range(self.top - self.height, self.top)
        domain = Domain(horz_range, vert_range)
        return Room(self.id, self.label, domain, HEIGHT)


class Plan(BaseModel):  # this should come from svg2plan
    rooms: list[RoomInPlan]

    @property
    def replan2eplus_rooms(self):
        return [i.as_replan2eplus_room for i in self.rooms]

    # as subsurface inputs..
