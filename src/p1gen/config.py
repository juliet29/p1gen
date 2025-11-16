from replan2eplus.ops.run_settings.user_interfaces import AnalysisPeriod
from p1gen.paths import CampaignNameOptions, DynamicPaths

CURRENT_CAMPAIGN: CampaignNameOptions = "20251116_palo_alto"
DEBUG_FIGURES = False
STUDY_DATE = (2017, 7, 1)
WEATHER_FILE = DynamicPaths.PALOALTO23
ANALYSIS_PERIOD = AnalysisPeriod("summer_cooling_season", 5, 8, 1, 1)
