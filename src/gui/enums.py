from enum import Enum, unique


@unique
class ArrayType(Enum):
    NONE       = -1
    RAW        =  0
    FILTERED   =  1
    NORMALISED =  2
    RATIO      =  3
    CLUSTER    =  4
    PHASE      =  5


# Same values as in plotTypeComboBox.
@unique
class PlotType(Enum):
    INVALID   = -1
    MAP       =  0
    HISTOGRAM =  1
    BOTH      =  2
