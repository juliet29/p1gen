from dataclasses import dataclass

from utils4plans.io import read_toml
from p1gen.paths import CampaignNameOptions, DynamicPaths
from rich import print
from pathlib import Path

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
        self.metadata["case"]

    @property
    def modifications(self):
        self.metadata["modifications"]


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


# @dataclass
# class CampaignStudy:

# def read_campaign_meta_data(name:CampaignNameOptions):
#     pass

if __name__ == "__main__":
    c = CampaignData("20251019_")
    # print(c.defn)
