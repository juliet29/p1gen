from typing import Literal
import polars as pl
import altair as alt


class AltairRenderers:
    BROWSER = "browser"


def create_fake_data():
    categories = ["window"] * 3 + ["door_vent_sched"] * 3 + ["material"] * 3
    options = (
        ["-30", "Default", "+30"]
        + ["Closed", "Dynamic", "Open"]
        + ["Light", "Medium", "Heavy"]
    )
    is_default = [False, True, False] + [False, False, True] + [False, True, False]
    avg = 10
    values = [avg - 2, avg, avg + 1] + [avg - 4, avg, avg + 5] + [avg - 6, avg, avg + 3]
    data = {
        "categories": categories,
        "options": options,
        "is_default": is_default,
        "values": values,
    }
    df = pl.DataFrame(data)
    return df


def plot_sensitivity(df: pl.DataFrame):
    # TODO this is where having a schema becomes useful..
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(x=alt.X("values"), y=alt.Y("categories"), color=alt.Color("categories"))
    )
    chart.show()


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)

    df = create_fake_data()
    plot_sensitivity(df)
