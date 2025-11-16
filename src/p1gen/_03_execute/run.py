from replan2eplus.ezcase.ez import EZ
from rich import print

from p1gen.paths import CampaignNameOptions, Constants
from p1gen._03_execute.interfaces import CampaignData

from p1gen.config import WEATHER_FILE, ANALYSIS_PERIOD


def run_experiments(campaign_name: CampaignNameOptions):
    meta_data_of_failures = []

    for exp in CampaignData(campaign_name).experiments:
        try:
            case = EZ(exp.path / Constants.IDF_NAME, read_existing=False)
            case.save_and_run(
                output_path=exp.path,
                epw_path=WEATHER_FILE,
                run=True,
                analysis_period=ANALYSIS_PERIOD,
                save=False,
            )  # TODO think this should also have a default weather

        except Exception as e:
            print(e)
            print(f"Running idf at {exp.path.name} failed!")
            meta_data_of_failures.append(exp.metadata)

        if len(meta_data_of_failures) >= 3:
            raise Exception(f"Too many failures.. stopping: {meta_data_of_failures}")

    print("Metadata of failed experiments:")
    print(meta_data_of_failures)


if __name__ == "__main__":
    run_experiments("20251116_palo_alto")
