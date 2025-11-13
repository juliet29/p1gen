import altair as alt
import polars as pl
from replan2eplus.ops.output.interfaces import OutputVariables

from p1gen.paths import CampaignNameOptions, DynamicPaths
from p1gen.plot_utils.utils import AltairRenderers
from p1gen._05_sensitivity.temperature_order import (
    CATEGORY_NAMES,
    DOOR_VENT,
    add_order_to_temp_df,
    ORDER,
)


def handle_df_filter(df: pl.DataFrame, dvent: bool = False):
    df1 = add_order_to_temp_df(df)
    if dvent:
        return df1.filter(pl.col.category == DOOR_VENT)
    return df1.filter(pl.col.category != DOOR_VENT)


def plot_sensitivity(
    df: pl.DataFrame, qoi: OutputVariables, unit: str, dvent: bool = False
):

    case_df = handle_df_filter(df, dvent)

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
    chart.show()


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)

    # df = create_data_set("20251109_summer", "Zone Mean Air Temperature")
    campaign_name: CampaignNameOptions = "20251112_summer_update_dv"
    df = pl.read_csv(
        source=DynamicPaths().get_path_for_comparison_data(campaign_name, "temperature")
    )

    c1 = plot_both(
        df,
        "Zone Mean Air Temperature",
        "C",
    )
