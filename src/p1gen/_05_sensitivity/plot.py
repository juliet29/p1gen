import polars as pl
import altair as alt
from p1gen.paths import DynamicPaths, CampaignNameOptions
from p1gen.plot_utils.utils import AltairRenderers
from replan2eplus.ops.output.interfaces import OutputVariables
from rich import print


def plot_sensitivity(df: pl.DataFrame, qoi: OutputVariables, unit: str):
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


def plot_sensitivity_dots(df: pl.DataFrame, qoi: OutputVariables, unit: str):
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


def plot_sensitivity_single(df: pl.DataFrame, qoi: OutputVariables, unit: str):
    df_constr = df.filter(pl.col("category") == "construction_set")
    df_window = df.filter(pl.col("category") == "window_dimension")
    df_door = df.filter(pl.col("category") == "door_vent_schedule")

    dfs = [df_constr, df_window, df_door]
    names = [
        "construction_set",
        "window_dimension",
        "door_vent_schedule",
    ]  # TODO get this from the defn passed in to genarate the data ..

    chart = alt.vconcat()
    for df, name in zip(dfs, names):
        row = (
            alt.Chart(df)
            .mark_point(size=100, filled=True)
            .encode(
                x=alt.X("value").scale(zero=False).title(f"{qoi} [{unit}]"),
                y=alt.Y("category"),
                color=alt.Color("option", legend=alt.Legend(title=name)),
                column=alt.Column("case"),
            )
            .resolve_axis(x="shared")
            .properties(height=50, width=300)
        )
        chart &= row

    chart2 = chart.resolve_scale(color="independent").resolve_axis(x="shared")
    chart2.show()
    return chart2


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)

    # df = create_data_set("20251109_summer", "Zone Mean Air Temperature")
    campaign_name: CampaignNameOptions = "20251109_summer"
    df = pl.read_csv(source=DynamicPaths().get_path_for_comparison_data(campaign_name))
    print(df)
    plot_sensitivity_single(df, "Zone Mean Air Temperature", "C")
