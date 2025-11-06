class CalcQOI:
    MIX_NET_HEAT_RATE = "AFN Zone Mixing Net Heat Exchange Rate"  # MINE!
    VENT_NET_HEAT_RATE = "AFN Zone Ventilation Net Heat Exchange Rate"
    NET_FLOW = "AFN Linkage Net Volume Flow Rate"
    MEDIAN_SITE_TEMP = "Median Site Temperature"
    ZONE_DEV_FROM_SITE_TEMP = "Zone Deviation from Site Temperature"


class Labels:
    NET_HEAT_EXCHANGE = "Net Heat Exchange Rate [W]"
    MIXVENT_VOLUME = "Volume [m3]"  #  averaged over # TODO time step transfer?
    SITE_TEMP = "Site Temp [ºC]"
    TEMP = "Temp [ºC]"
    DEVIATION_FROM_SITE_TEMP = "Deviation from Site Temp [ºC]"


class DFC:
    """Dataframe Columns"""

    CASE_NAMES = "case_names"
    SPACE_NAMES = "space_names"

    DATETIMES = "datetimes"
    HOUR = "hour"
    TIME = "time"

    ZONE = "zone"
    DIRECTION = "direction"
    IS_EXTERIOR = "is_exterior"

    # after pivoting for altair
    VARIABLE = "variable"
    VALUE = "value"
