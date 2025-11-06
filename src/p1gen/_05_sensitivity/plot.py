from typing import Literal
import polars as pl
import altair as alt
from p1gen.sensitivity.data import create_data_set
from p1gen.paths import CampaignNameOptions
from p1gen.plot_utils.qois import QOI
from p1gen.plot_utils.utils import AltairRenderers




def plot_sensitivity(df: pl.DataFrame, qoi: str, unit: str):
    case_df = df.with_columns(
        pl.when(pl.col.option == pl.lit("Default"))
        .then(True)
        .otherwise(False)
        .alias("IsDefault")
    )
    line = (
        alt.Chart(case_df)
        .transform_calculate(
            res=alt.expr.if_(alt.datum.IsDefault == True, "black", "white")
        )
        .mark_line(point=alt.OverlayMarkDef(filled=True, color="res", size=100))
        .encode(
            x=alt.X("value").scale(zero=False).title(f"{qoi} [{unit}]"),
            y=alt.Y("category"),
            color=alt.Color("category"),
            column=alt.Column("case"),
        )
        .resolve_axis(x="shared")
        .properties(height=100, width=400)
    )
    line.show()

    return line  # + circles


def plot_sensitivity_dots(df: pl.DataFrame, qoi: str, unit: str):
    case_df = df.with_columns(
        pl.when(pl.col.option == pl.lit("Default"))
        .then(True)
        .otherwise(False)
        .alias("IsDefault")
    )
    line = (
        alt.Chart(case_df)
        .transform_calculate(
            res=alt.expr.if_(alt.datum.IsDefault == True, "black", "white")
        )
        .mark_point(size=100, filled=True)
        .encode(
            x=alt.X("value").scale(zero=False).title(f"{qoi} [{unit}]"),
            y=alt.Y("category"),
            color=alt.Color("option"),
            column=alt.Column("case"),
        )
        .resolve_axis(x="shared")
        .properties(height=100, width=400)
    )
    line.show()

    return line  # + circles


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)

    df = create_data_set("20251020_NoAFN", QOI.VENT_VOL)
    plot_sensitivity_dots(df, QOI.VENT_VOL, "m3/s")
