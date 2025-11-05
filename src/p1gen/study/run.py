from p1gen.paths import Constants, ep_paths, CampaignNameOptions
from p1gen.study.interfaces import CampaignData, Experiment
from replan2eplus.idfobjects.idf import IDF
from pathlib import Path
from typing import NamedTuple
from rich import print


class IDFAndPath(NamedTuple):
    idf: IDF
    path: Path


def run_experiments(campaign_name: CampaignNameOptions):
    # IDF.iddname(ep_paths.idd_path)
    def create_idf(path: Path):
        return IDF(
            ep_paths.idd_path,
            path / Constants.IDF_NAME,
            ep_paths.default_weather,  # TODO: shouldnt have to specify the wearher of ep path again really..
        )

    def run_idf(idf: IDF, path: Path):
        idf.idf.run(output_directory=path / Constants.RESULTS_DIR)

    CD = CampaignData(campaign_name)

    idf_and_paths = [
        IDFAndPath(create_idf(exp.path), exp.path) for exp in CD.experiments
    ]

    meta_data_of_failures = []

    for idf, path in idf_and_paths:
        try:
            run_idf(idf, path)
        except:
            print(f"Running idf at {path.name} failed!")
            meta_data_of_failures.append(Experiment(path).metadata)
        if len(meta_data_of_failures) > 3:
            raise Exception(f"Too many failures.. stopping: {meta_data_of_failures}")

    print("Metadata of failed experiments:")
    print(meta_data_of_failures)


if __name__ == "__main__":
    run_experiments("20251020_AFN")
