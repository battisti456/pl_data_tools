from dataclasses import fields
from datetime import datetime
from typing import Any, Callable, Literal, Sequence, Union, get_args

import numpy as np

from .pl_data_row import (
    PL_Data_Row,
    PL_Data_Row_Area_Scan,
    PL_Data_Row_Line_Scan,
    PL_Data_Row_Transmit_Time,
    _Row_Beginning,
    _Row_Data_Area_Scan,
    _Row_Data_Line_Scan,
    _Row_Data_Transmit_Time,
    _Row_Ending,
)


def line_to_data(line:Sequence[str]) -> 'PL_Data_Row':
    cls:type|None = None
    kwargs:dict[str,Any] = {}
    fds = list(fields(_Row_Beginning))
    item_iter = line.__iter__()
    for item,field in zip(item_iter,fds):
        tp = field.type
        if hasattr(tp, '__origin__') and getattr(tp, "__origin__") is Union:
            tp = get_args(tp)[0]
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
                case 'Line Scan':
                    cls = PL_Data_Row_Line_Scan
                    fds.extend(fields(_Row_Data_Line_Scan))
                case _:
                    raise Exception(f"Encountered unknown measurement type '{item}'.")
            fds.extend(fields(_Row_Ending)[:-1])#exit before signal
    if cls is None:
        raise Exception("Row did not contain sufficient columns.")
    comment:str = kwargs['Comment']
    comment = comment.replace('&quot','"')#correct pl quotation mark signature
    comment = comment.replace('&#13','')#remove pl newline signature
    kwargs['Comment'] = comment
    i = len(fields(cls)) - 1
    kwargs['Signal'] = np.array(
        object=line[i:i+kwargs['Signal_Size']],
        dtype=np.int16
    )
    return cls(**kwargs)