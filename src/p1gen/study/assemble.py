from dataclasses import dataclass
from typing import NamedTuple
from ladybug.sql import SQLiteResult
from replan2eplus.ezcase.read import ExistCase
from p1gen.paths import CampaignNameOptions, Constants
from p1gen.study.interfaces import Experiment, CampaignData
from utils4plans.lists import chain_flatten
from rich import print
from copy import deepcopy


class ComparisonData(NamedTuple):
    case: str
    category: str
    option: str
    sql: SQLiteResult

    @property
    def description(self):
        d = {"case": self.case, "category": self.category, "option": self.option}
        return d


def assemble_comparison_data(
    campaign_name: CampaignNameOptions,
) -> list[ComparisonData]:
    def create_comparison_data(exp: Experiment):
        if not exp.modifications:
            option = Constants.DEFAULT_OPTION
            return [
                ComparisonData(exp.case_name, category, option, exp.sql_results)
                for category in campaign_data.modification_categories
            ]

        # baseline
        return [
            ComparisonData(exp.case_name, exp.category, exp.option, exp.sql_results)
        ]

    campaign_data = CampaignData(campaign_name)
    results = [create_comparison_data(e) for e in campaign_data.experiments]
    r = chain_flatten(results)

    return r


if __name__ == "__main__":
    print(assemble_comparison_data("20251020_NoAFN"))
