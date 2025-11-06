from replan2eplus.results.sql import (
    create_result_for_qoi,
    SQLiteResult,
)
from p1gen.plot_utils.qois import QOI
from p1gen._03_execute.interfaces import CampaignData
from p1gen.paths import CampaignNameOptions
from p1gen._03_execute.assemble import assemble_comparison_data
from typing import NamedTuple
import polars as pl
from rich import print


class DataSetInputs(NamedTuple):
    case: str
    category: str
    option: str
    value: float


def get_space_and_time_avg_for_qoi(sql: SQLiteResult, qoi: str):
    qoi_res = create_result_for_qoi(sql, qoi)
    data = qoi_res.data_arr
    return float(data.mean())


def create_data_set(name: CampaignNameOptions, qoi: str):
    comparison_data = assemble_comparison_data(name)

    results = [
        DataSetInputs(**i.description, value=get_space_and_time_avg_for_qoi(i.sql, qoi))
        for i in comparison_data
    ]
    return pl.DataFrame(results)


if __name__ == "__main__":
    # c = CampaignData("20251020_NoAFN")
    # exp = c.experiments[0]
    # res = get_space_and_time_avg_temp(exp.sql_results)
    res = create_data_set("20251020_NoAFN", QOI.TEMP)
