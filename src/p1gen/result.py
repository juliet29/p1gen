from p1gen.analysis.deviation import plot_deviation_cases
from p1gen.analysis.utils import AltairRenderers
import altair as alt
from replan2eplus.examples.plots.data_plot import plot_zones_and_connections
from p1gen.paths import ep_paths
from p1gen._03_execute.interfaces import CampaignData
from p1gen.analysis.time_series import (
    plot_exp_results,
    prepare_vol_df,
    prepare_temp_df,
    prepare_heat_df,
)
from p1gen.analysis.qois import Labels


def plot_geoms():
    c = CampaignData("20251020_NoAFN")
    exps = [i for i in c.experiments if not i.modifications]
    for exp in exps:
        print(exp.case_name)
        res = plot_zones_and_connections(ep_paths.idd_path, exp.path, hour=12)
        res.show()


def main():
    # chart = plot_deviation_cases()
    # chart.show()

    chart = plot_exp_results(Labels.TEMP, prepare_temp_df)
    chart.show()


if __name__ == "__main__":
    alt.renderers.enable(AltairRenderers.BROWSER)
    main()
    # plot_geoms()
