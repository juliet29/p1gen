import altair as alt
import polars as pl
from replan2eplus.ops.output.interfaces import OutputVariables

from p1gen.paths import CampaignNameOptions
from p1gen.plot_utils.utils import AltairRenderers
from p1gen.plot_utils.save import save_figure
from p1gen.sensitivity.temperature_order import (
    CATEGORY_NAMES,
    DOOR_VENT,
    add_order_to_temp_df,
    ORDER,
)
from p1gen.config import CURRENT_CAMPAIGN, DEBUG_FIGURES
from p1gen.sensitivity.data import create_data_set


def handle_df_filter(df: pl.DataFrame, dvent: bool = False, dont_split: bool = False):
    df1 = add_order_to_temp_df(df)
    if dont_split:
        return df1
    if dvent:
        return df1.filter(pl.col.category == DOOR_VENT)
    return df1.filter(pl.col.category != DOOR_VENT)


def plot_sensitivity(
    df: pl.DataFrame,
    qoi: OutputVariables | str,
    unit: str,
    dvent: bool = False,
    dont_split: bool = False,
):

    case_df = handle_df_filter(df, dvent, dont_split)

    chart = (
        alt.Chart(case_df)
        .mark_line(point=alt.OverlayMarkDef(filled=True, color="res", size=100))
        .encode(
            x=alt.X("value").scale(zero=False).title(f"{qoi} [{unit}]"),
            y=alt.Y(f"{CATEGORY_NAMES}:N").title(None),
            color=alt.Color("category").legend(None),
            shape=alt.Shape(f"{ORDER}:O").legend(None),
            row=alt.Row("case").title(None).header(labelFontSize=15, labelAngle=0),
        )
        .resolve_axis(x="shared")
        .properties(height=50, width=400)
    )

    return chart  # + circles


def plot_both(df: pl.DataFrame, qoi: OutputVariables, unit: str):
    c1 = plot_sensitivity(df, qoi, unit)
    c2 = plot_sensitivity(
        df, qoi, unit, dvent=True
    )  # .configure_axisY(labels=False, title=None)
    chart = c1 | c2
    return chart


@save_figure(CURRENT_CAMPAIGN, "sens_flow", DEBUG_FIGURES)
def make_sensitivity_flow_plot(campaign_name: CampaignNameOptions):
    df = create_data_set(campaign_name, "AFN Linkage Node 1 to Node 2 Volume Flow Rate")
    chart = plot_sensitivity(df, "Flow Rate", "m3/s", dont_split=True)
    return chart


@save_figure(CURRENT_CAMPAIGN, "sens_temp", DEBUG_FIGURES)
def make_sensitivity_temp_plot(campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN):
    df = create_data_set(campaign_name, "Zone Mean Air Temperature")

    chart = plot_both(
        df,
        "Zone Mean Air Temperature",
        "C",
    )
    return chart


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)

    campaign_name: CampaignNameOptions = CURRENT_CAMPAIGN
    df = create_data_set(CURRENT_CAMPAIGN, "Zone Mean Air Temperature")
    # df = pl.read_csv(
    #     source=DynamicPaths().get_path_for_comparison_data(campaign_name, "temperature")
    # )
    #
    # c1 = plot_both(
    #     df,
    #     "Zone Mean Air Temperature",
    #     "C",
    # )
