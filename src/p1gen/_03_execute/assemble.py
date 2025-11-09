from typing import NamedTuple
from pathlib import Path
from p1gen.paths import CampaignNameOptions, Constants
from p1gen._03_execute.interfaces import Experiment, CampaignData
from utils4plans.lists import chain_flatten
from rich import print


class ComparisonData(NamedTuple):
    case_name: str
    category: str
    option: str
    # sql: SQLiteResult
    path: Path
    # ezcase: EZ

    @property
    def description(self):
        d = {"case": self.case_name, "category": self.category, "option": self.option}
        return d


class ComparisonDataList(NamedTuple):
    values: list[
        ComparisonData
    ]  # this is a bit redundant now, since we are returning values elsewhere..


def assemble_default_data(campaign_name: CampaignNameOptions):
    def create(exp: Experiment):
        return ComparisonData(
            exp.case_name,
            Constants.DEFAULT_CATEGORY,
            Constants.DEFAULT_OPTION,
            # exp.sql_results,
            exp.path,
            # exp.ezcase,
        )

    return [
        create(e)
        for e in CampaignData(campaign_name).experiments
        if not e.category and not e.modifications
    ]


def assemble_comparison_data(
    campaign_name: CampaignNameOptions,
):
    def create(exp: Experiment):
        if not exp.modifications:
            option = Constants.DEFAULT_OPTION
            return [
                ComparisonData(
                    exp.case_name,
                    category,
                    option,
                    # exp.sql_results,
                    exp.path,
                    # exp.ezcase,
                )
                for category in campaign_data.modification_categories
            ]

        # baseline
        return [
            ComparisonData(
                exp.case_name,
                exp.category,
                exp.option,
                # exp.sql_results,
                exp.path,
                # exp.ezcase,
            )
        ]

    campaign_data = CampaignData(campaign_name)
    results = [create(e) for e in campaign_data.experiments]
    r = chain_flatten(results)

    return r


if __name__ == "__main__":
    print(assemble_default_data("20251105_door_sched"))
