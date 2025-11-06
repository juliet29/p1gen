class QOI:
    # site
    WIND_SPEED = "Site Wind Speed"
    WIND_DIRECTION = "Site Wind Direction"
    SITE_TEMP = "Site Outdoor Air Drybulb Temperature"

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
    VENT_AFN = "AFN Zone Ventilation Air Change Rate"
    # surface like..
    WIND_PRESSURE = ""  # TODO!
