from replan2eplus.ops.run_settings.user_interfaces import AnalysisPeriod
from p1gen.paths import CampaignNameOptions, DynamicPaths

CURRENT_CAMPAIGN: CampaignNameOptions = "20251116_palo_alto24"
DEBUG_FIGURES = False
STUDY_DATE = (2017, 7, 1)
STUDY_HOUR = 12
WEATHER_FILE = (
    DynamicPaths.PALOALTO24
)  # ep_paths.default_weather  # DynamicPaths.PALOALTO24
ANALYSIS_PERIOD = AnalysisPeriod("summer_cooling_season", 6, 10, 1, 31)
