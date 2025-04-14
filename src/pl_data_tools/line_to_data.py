from dataclasses import fields
from datetime import datetime
from typing import Any, Callable, Literal, Optional, Sequence

import numpy as np

from .pl_data_row import (
    PL_Data_Row,
    PL_Data_Row_Area_Scan,
    PL_Data_Row_Transmit_Time,
    _Row_Beginning,
    _Row_Data_Area_Scan,
    _Row_Data_Transmit_Time,
    _Row_Ending,
)


def line_to_data(line:Sequence[str]) -> 'PL_Data_Row':
    cls:type|None = None
    kwargs:dict[str,Any] = {}
    fds = list(fields(_Row_Beginning))
    signal_values = line[len(fds)-1:]
    for item,field in zip(line,fds):
        tp = field.type
        if tp is Optional:
            tp = tp.__args__[0]#type:ignore
        if tp is str:
            kwargs[field.name] = item
        elif item == '--':
            kwargs[field.name] = None
        elif hasattr(tp, '__origin__') and getattr(tp, "__origin__") is Literal:
            kwargs[field.name] = item
        elif tp is bool:
            kwargs[field.name] = item == 'Y'
        elif tp is datetime:
            kwargs[field.name] = datetime.fromisoformat(item)
        else:
            assert isinstance(tp,Callable)
            try:
                kwargs[field.name] = tp(item)
            except TypeError as e:
                e.add_note(f"'{item}' could not be interpreted as '{tp}'")
                raise e
        if field.name == 'Meas_Type':
            match(item):
                case 'Transmission Time':
                    cls = PL_Data_Row_Transmit_Time
                    fds.extend(fields(_Row_Data_Transmit_Time))
                case 'Area Scan':
                    cls = PL_Data_Row_Area_Scan
                    fds.extend(fields(_Row_Data_Area_Scan))
                case _:
                    raise Exception(f"Encountered unknown measurement type '{item}'.")
            fds.extend(fields(_Row_Ending)[:-1])#exit before signal

    signal = np.zeros(
        shape = (kwargs['Signal_Size']),
        dtype = np.int16
    )
    signal[:] = np.array(signal_values)
    kwargs['Signal'] = signal
    if cls is None:
        raise Exception("Row did not contain sufficient columns.")
    return cls(**kwargs)