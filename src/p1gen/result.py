from p1gen.plot_utils.utils import AltairRenderers
import altair as alt
from replan2eplus.ex.make import make_data_plot
from p1gen.paths import ep_paths
from p1gen._03_execute.interfaces import CampaignData
from p1gen.analysis.time_series import (
    plot_exp_results,
    prepare_temp_df,
)
from p1gen.plot_utils.labels import Labels


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
