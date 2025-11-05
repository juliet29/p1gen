from dataclasses import dataclass

from utils4plans.io import read_toml
from p1gen.paths import CampaignNameOptions, DynamicPaths, ep_paths, Constants
from rich import print
from pathlib import Path
from replan2eplus.results.sql import get_sql_results
from replan2eplus.ezcase.ez import EZ

METADATA = "metadata.toml"
DEFINITION = "defn.toml"


@dataclass
class Experiment:
    path: Path
    # campaign_path: Path
    # name: str
    # # index: int

    # # @property
    # # def number_name(self):
    # #     return
    # @property
    # def path(self):
    #     return self.campaign_path / self.name

    @property
    def metadata(self):
        return read_toml(self.path, METADATA)

    @property
    def case(self):
        return self.metadata["case"]

    @property
    def modifications(self):
        return self.metadata["modifications"]

    @property
    def category(self):
        # assuming only one for now..
        if self.modifications:
            return list(self.modifications.keys())[0]
        return ""

    @property
    def option(self):
        # assuming only one for now..
        if self.modifications:
            return list(self.modifications.values())[0]
        return ""

    @property
    def ezcase(self):
        return EZ(idf_path=self.path / Constants.IDF_NAME)

    @property
    def sql_results(self):
        try:
            return get_sql_results(self.path)
        except AssertionError:
            raise Exception(
                f"Could not find sql results for {self.path.parent.name} / {self.path.name}"
            )


@dataclass
class CampaignData:
    # c1019 = "20251019_"
    name: CampaignNameOptions

    @property
    def path(self):
        return DynamicPaths.CAMPAIGN / self.name

    @property
    def metadata(self):
        return read_toml(self.path, METADATA)

    @property
    def defn(self):
        return read_toml(self.path, DEFINITION)

    @property
    def experiments(self):
        return [Experiment(i) for i in self.path.iterdir() if i.is_dir()]

    @property
    def modification_categories(self):
        return [i["name"] for i in self.defn["modifications"]]


# @dataclass
# class CampaignStudy:

# def read_campaign_meta_data(name:CampaignNameOptions):
#     pass

if __name__ == "__main__":
    c = CampaignData("20251019_")
    # print(c.defn)
