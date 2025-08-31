import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, ConnectionStyle, ArrowStyle
from matplotlib.path import Path
from matplotlib.lines import Line2D
from typing import NamedTuple
from copy import deepcopy

# Create a figure and an axes object
# fig, ax = plt.subplots()


def get_xys(xys: list[tuple[int, int]]):
    return [i[0] for i in xys], [i[1] for i in xys]


# vertices = [(1, 0), (1, 1), (2, 2)]
# x, y = get_xys(vertices)
# print(x, y)
# line = Line2D(x, y, linewidth=5, color="pink", zorder=0)
# # codes = None


# # arrow_path = Path(vertices[1:2])

# arrow_style = ArrowStyle("Simple", head_length=10, head_width=15, tail_width=2)

# fancy_arrow = FancyArrowPatch(
#     posA=vertices[1],
#     posB=vertices[2],
#     color="black",
#     shrinkB=20,
#     arrowstyle=arrow_style,
#     mutation_scale=1,
#     zorder=1,
# )
# ax.add_artist(fancy_arrow)
# ax.add_artist(line)

# ax.set_xlim(0, 5)
# ax.set_ylim(0, 5)
# plt.show()


class ArrowStyleParams(NamedTuple):
    head_length: int = 15
    head_width: int = 20
    tail_width: int = 2
    shrink: int = 20


# TODO also have scale -> assoc with size and color
def create_connection_patch(
    line_: Line2D,
    is_negative: bool,
    color,
    width,
    arrow_styles: ArrowStyleParams = ArrowStyleParams(),
):
    width = width/ 5
    line = deepcopy(line_)
    xydata = line.get_xydata()

    posA, posB = xydata[1], xydata[2]

    if is_negative:
        posA, posB = xydata[1], xydata[0]

    # assert len(coords) == 3
    # x, y = get_xys(vertices)
    # line = Line2D(x, y, linewidth=LINEWIDTH, color="pink")

    arrow_style = ArrowStyle(
        "Simple",
        head_length=arrow_styles.head_length * width,
        head_width=arrow_styles.head_width * width,
        tail_width=arrow_styles.tail_width * width,
    )
    fancy_arrow = FancyArrowPatch(
        posA=posA,
        posB=posB,
        color="black",
        shrinkA=arrow_styles.shrink*1.8 ,
        shrinkB=arrow_styles.shrink ,
        arrowstyle=arrow_style,
        zorder=5,
   
    )

    return fancy_arrow


if __name__ == "__main__":
    x = [0, 0, 1]
    y = [0, 1, 1]
    line = Line2D(x, y)
    create_connection_patch(line, True, "orange")
