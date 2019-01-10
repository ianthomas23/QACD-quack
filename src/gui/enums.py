from enum import Enum, unique


@unique
class ArrayType(Enum):
    INVALID    = -1
    RAW        =  0
    FILTERED   =  1
    NORMALISED =  2
    RATIO      =  3
    CLUSTER    =  4
    PHASE      =  5
    REGION     =  6


@unique
class ModeType(Enum):
    INVALID          = 0
    ZOOM             = 1
    REGION_RECTANGLE = 2
    REGION_ELLIPSE   = 3
    REGION_POLYGON   = 4
    TRANSECT         = 5


# Same values as in plotTypeComboBox.
@unique
class PlotType(Enum):
    INVALID           = -1
    MAP               =  0
    HISTOGRAM         =  1
    MAP_AND_HISTOGRAM =  2
    MAP_AND_TRANSECT  =  3
