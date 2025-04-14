from dataclasses import dataclass

import numpy as np


@dataclass
class PL_Data:
    PL_Link_Version:str
    Name:str
    Serial_Number:str
    Software_Version:str
    Hardware_Revision:str
    Maximum:np.int16
    Minimum:np.int16
    Meas_Range:str
    Step_Size:str
    Folder:str