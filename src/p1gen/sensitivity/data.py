from replan2eplus.results.sql import (
    create_result_for_qoi,
)
from utils4plans.io import check_folder_exists_and_return, get_or_make_folder_path
from pathlib import Path
from p1gen.config import CURRENT_CAMPAIGN
from p1gen.paths import CampaignNameOptions, get_sqlite_object, DynamicPaths
from p1gen._03_execute.assemble import assemble_comparison_data
from typing import NamedTuple
from replan2eplus.ops.output.interfaces import OutputVariables
import polars as pl
from p1gen._03_execute.zone_size import get_afn_zone_names


class DataSetInputs(NamedTuple):
    case: str
    category: str
    option: str
    value: float


def get_space_and_time_avg_for_qoi(path: Path, qoi: OutputVariables):
    sql = get_sqlite_object(path)
    qoi_res = create_result_for_qoi(sql, qoi)
    data = qoi_res.data_arr
    if qoi == "Zone Mean Air Temperature":
        afn_zone_names = get_afn_zone_names(path)
        afn_filter = data.space_names.isin(afn_zone_names)
        afn_data = data.sel(space_names=afn_filter)
        return float(afn_data.mean())

    return float(data.mean())


def create_data_set(name: CampaignNameOptions, qoi: OutputVariables):
    comparison_data = assemble_comparison_data(name)

    results = []
    for exp in comparison_data:
        print(exp.case_name, exp.category, exp.option)
        data = DataSetInputs(
            **exp.description,
            value=get_space_and_time_avg_for_qoi(exp.path, qoi),
        )
        results.append(data)

    # results = [
    #     DataSetInputs(
    #         **i.description,
    #         value=get_space_and_time_avg_for_qoi(get_sqlite_object(i.path), qoi),
    #     )
    #     for i in comparison_data.values
    # ]
    return pl.DataFrame(results)


def write_dataframe(
    df: pl.DataFrame, path: Path
):  # TODO: add this to utils4plans, and update other io paths to match this paradigm
    exist_path = check_folder_exists_and_return(path.parent.parent)
    res = get_or_make_folder_path(exist_path, str(path.parent))
    final_path = res / path.name
    df.write_csv(final_path)
    # TODO test this!


if __name__ == "__main__":
    # c = CampaignData("20251020_NoAFN")
    # exp = c.experiments[0]
    # res = get_space_and_time_avg_temp(exp.sql_results)

    campaign: CampaignNameOptions = CURRENT_CAMPAIGN

    wpath = DynamicPaths().get_path_for_comparison_data(campaign, "temperature")
    assert wpath.parent.exists(), f"Path does not exist:{wpath.parent}"
    res = create_data_set(campaign, "Zone Mean Air Temperature")
    write_dataframe(res, wpath)
    #
    # print(res)
    # fake_df = pl.DataFrame({"hi": [1, 2, 3]})
