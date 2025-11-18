import polars as pl
import matplotlib.pyplot as plt
import altair as alt
from typing import Protocol
from p1gen.paths import CampaignNameOptions, static_paths, FigureNames
from utils4plans.io import create_time_string, get_or_make_folder_path
from matplotlib.figure import Figure


AltairChart = (
    alt.Chart | alt.HConcatChart | alt.VConcatChart | alt.FacetChart | alt.ConcatChart
)


class ReturnsChart(Protocol):
    def __call__(self, *args, **kwargs) -> AltairChart | Figure: ...


def make_figure_path(campaign_name: CampaignNameOptions, figure_name: FigureNames):
    parent_path = get_or_make_folder_path(static_paths.figures, str(campaign_name))
    time = create_time_string()
    suffix = ".png"
    new_name = f"{figure_name}_{time}{suffix}"
    return parent_path / new_name


def save_figure(
    campaign_name: CampaignNameOptions, figure_name: FigureNames, debug: bool = True
):
    def decorator_save_figure(func: ReturnsChart):
        def wrapper(*args, **kwargs):
            chart = func(*args, **kwargs)
            if debug:
                if isinstance(chart, Figure):
                    plt.show()
                else:
                    chart.show()

            else:
                save_path = make_figure_path(campaign_name, figure_name)
                if isinstance(chart, Figure):
                    chart.set_layout_engine("constrained")
                    chart.savefig(save_path, dpi=300)
                else:
                    chart.save(save_path, ppi=300)

            return

        return wrapper

    return decorator_save_figure


@save_figure("test", "test", debug=True)
def test_mpl_chart():
    fig, ax = plt.subplots()  # Create a figure containing a single Axes.
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the Axes.

    return fig


@save_figure("test", "test", debug=False)
def test_chart():
    data = pl.DataFrame({"x": ["A", "B", "C", "D", "E"], "y": [5, 3, 6, 7, 2]})
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x="x",
            y="y",
        )
    )

    return chart


if __name__ == "__main__":
    test_mpl_chart()
