

from p1gen.utils import read_idf
from p1gen.paths import test_case
from p1gen.geom_plot import create_geom_plot
from p1gen.read_sql import get_sql_results
from p1gen.data_helpers import create_dataframe_for_case


class QOI:
    # site 
    WIND_SPEED = "Site Wind Speed"
    WIND_DIRECTION = "Site Wind Direction"
    SITE_TEMP = "Site Outdoor Air Drybulb Temperature,"




    # zone level 
    TEMP = "Zone Mean Air Temperature"
    VENT_VOL = "AFN Zone Ventilation Volume"
    MIX_VOL = "AFN Zone Mixing Volume"
    NODE_PRESSURE = "AFN Node Total Pressure"

    # subsurface / surface
    FLOW_12 = "AFN Linkage Node 1 to Node 2 Volume Flow Rate"
    FLOW_21 = "AFN Linkage Node 2 to Node 1 Volume Flow Rate"

    # surface like.. 
    WIND_PRESSURE = "" # TODO! 






if __name__ == "__main__":
    case = read_idf(test_case)
    sql_results = get_sql_results(test_case)
    # flow_df = create_dataframe_for_case(sql_results, [QOI.FLOW_12, QOI.FLOW_21], case)
    # print(flow_df)


    # vol_df = create_dataframe_for_case(sql_results, [QOI.MIX_VOL, QOI.VENT_VOL], case)
    # print(vol_df)

    pressure_df = create_dataframe_for_case(sql_results, [QOI.NODE_PRESSURE], case)
    print(pressure_df)
    # create_geom_plot(case)