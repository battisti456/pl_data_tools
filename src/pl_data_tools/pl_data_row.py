from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional, TypeVar

import numpy as np


#region prototypes
#region universal prototypes
@dataclass
class _Row_Beginning:
    SW_Version:str
    Meas_Type:Literal['Area Scan', 'Transmission Time']
    Result:Optional[str]
    Name:str
    Data_and_Time:datetime
    No_of_Meas:int
@dataclass
class _Row_Ending:
    Meas_Range:Literal['Short','Long']
    Probe_Freq:int
    Probe_Type:Literal['P-wave','S-wave','Exponential']
    Probe_Gain:int
    Probe_Voltage:int
    PRF:int
    Calib_Time:float
    Correction_Factor:float
    Time_Gain:bool
    Unit:Literal['Metric','Imperial']
    Amplitude:Literal['dB']
    Compr_Strength_Unit:Optional[str]
    Trigger:Literal['auto','manual']
    Trigger_Amplitude:float
    Marker_Amplitude:Optional[float]
    Transmission:Literal['Burst','Continuous']
    Gate_enabled:bool
    Gate_start:int
    Gate_stop:int
    Comment:str
    Signal_Size:int
    Signal:np.ndarray[tuple[int],np.dtype[np.int16]]
#endregion
#region type prototypes
@dataclass
class _Row_Data_Transmit_Time:
    Time_1:float
    Time_2:float
@dataclass
class _Row_Data_Area_Scan:
    Meas:int
    Measurement_Count_X:int
    Measurement_Count_Y:int
    Raster_X:float
    Raster_Y:float
    _Result:Literal['Time']
    Distance0:Optional[float]
    Velocity0:Optional[float]
    Color_Scheme:Literal['Green Smooth']
    Auto_Color_Range:bool
    Minimum:float
    Maximum:float
    X:float
    Y:float
    Time_1:float
    Distance1:Optional[float]
    Velocity1:Optional[float]
#endregion
#endregion
#region subclasses
class PL_Data_Row_Transmit_Time(
    _Row_Beginning,
    _Row_Data_Transmit_Time,
    _Row_Ending
):
    ...
class PL_Data_Row_Area_Scan(
    _Row_Beginning,
    _Row_Data_Area_Scan,
    _Row_Ending
):
    ...
type PL_Data_Row = PL_Data_Row_Transmit_Time|PL_Data_Row_Area_Scan
PL_Data_Row_Var = TypeVar('PL_Data_Row_Var',PL_Data_Row_Transmit_Time,PL_Data_Row_Area_Scan)
#endregion
