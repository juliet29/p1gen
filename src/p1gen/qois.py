
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


class Labels:
    NET_HEAT_EXCHANGE = "Net Heat Exchange Rate [W]"
    MIXVENT_VOLUME = "Volume [m3]"  #  averaged over # TODO time step transfer?


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

    MIX_HEAT_GAIN_RATE = "AFN Zone Mixing Sensible Heat Gain Rate"
    MIX_HEAT_LOSS_RATE = "AFN Zone Mixing Sensible Heat Loss Rate"

    VENT_HEAT_GAIN_RATE = "AFN Zone Ventilation Sensible Heat Gain Rate"
    VENT_HEAT_LOSS_RATE = "AFN Zone Ventilation Sensible Heat Loss Rate"

    # subsurface / surface
    FLOW_12 = "AFN Linkage Node 1 to Node 2 Volume Flow Rate"
    FLOW_21 = "AFN Linkage Node 2 to Node 1 Volume Flow Rate"

    # surface like..
    WIND_PRESSURE = ""  # TODO!


class CalcQOI:
    MIX_NET_HEAT_RATE = "AFN Zone Mixing Net Heat Exchange Rate"  # MINE!
    VENT_NET_HEAT_RATE = "AFN Zone Ventilation Net Heat Exchange Rate"
    NET_FLOW = "AFN Linkage Net Volume Flow Rate"

