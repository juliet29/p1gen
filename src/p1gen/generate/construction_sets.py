from typing import Literal
from replan2eplus.ezobjects.construction import EPConstructionSet, BaseConstructionSet

MaterialTypes = Literal["Light", "Medium", "Heavy"]


def create_constructions_sets(material_type: MaterialTypes):
    return EPConstructionSet(
        # interior then exterior
        wall=BaseConstructionSet(
            f"{material_type} Partitions", f"{material_type} Exterior Wall"
        ),
        floor=BaseConstructionSet(f"{material_type} Floor", f"{material_type} Floor"),
        roof=BaseConstructionSet(
            f"{material_type} Roof/Ceiling", f"{material_type} Roof/Ceiling"
        ),
        window=BaseConstructionSet("Sgl Clr 6mm", "Sgl Clr 6mm"),
        door=BaseConstructionSet(
            f"{material_type} Furnishings", f"{material_type} Furnishings"
        ),
    )
