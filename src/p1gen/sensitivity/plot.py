from typing import Literal
import polars as pl
import altair as alt
from p1gen.sensitivity.data import create_data_set
from p1gen.paths import CampaignNameOptions
from p1gen.analysis.qois import QOI


class AltairRenderers:
    BROWSER = "browser"


def plot_sensitivity(df: pl.DataFrame, qoi: str, unit: str):
    def create_case_chart(case_name: str):
        case_df = df.with_columns(
            pl.when(pl.col.option == pl.lit("Default"))
            .then(True)
            .otherwise(False)
            .alias("IsDefault")
        ).filter(pl.col.case == case_name)

        encoding = alt.Chart(case_df).encode(
            x=alt.X("value").scale(zero=False).title(f"{qoi} [{unit}]"),
            y=alt.Y("category"),
        )
        line = encoding.mark_line().encode(
            # x=alt.X("value").scale(zero=False).title(f"{qoi} [{unit}]"),
            # y=alt.Y("category"),
            color=alt.Color("category"),
        )  # .resolve_axis(x="shared")

        label = alt.datum.IsDefault
        color_coding = (
            (alt.when(label)).then(alt.value("black")).otherwise(alt.value("white"))
        )
        circles = encoding.mark_circle().encode(color=color_coding)
        return line + circles

        # chart = (line + circles).properties(height=100, width=400)

    charts = [create_case_chart(i) for i in ["A", "B", "C"]]
    charts[2].show()
    # c = (
    #     alt.HConcatChart(charts)
    #     # .properties(height=100, width=400)
    #     # .resolve_axis(x="shared")
    # )
    # c.show()


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)

    df = create_data_set("20251020_NoAFN", QOI.TEMP)
    plot_sensitivity(df, QOI.TEMP, "ºC")
