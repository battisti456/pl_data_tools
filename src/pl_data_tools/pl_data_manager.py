import os
from dataclasses import dataclass
from typing import Any, Iterator, Optional

import numpy as np

from .line_to_data import line_to_data
from .pl_csv_reader import NUMBER_ROWS_IN_HEADER, PL_CSV_Reader
from .pl_data import PL_Data
from .pl_data_row import PL_Data_Row


@dataclass
class PL_Data_Manager(PL_Data):
    _path:Optional[str|os.PathLike] = None
    _length:Optional[int] = None
    @classmethod
    def _load(cls,path:str|os.PathLike):
        """Loads a Proceq PL-Link exported csv as a python dataclass

        Args:
            path: path to .csv
        """
        kwargs:dict[str,Any] = {"_path":path}
        with PL_CSV_Reader(path) as reader:
            kwargs['PL_Link_Version'] = next(reader)[1]
            next(reader)#Device Data
            kwargs['Name'] = next(reader)[1]
            kwargs['Serial_Number'] = next(reader)[1]
            kwargs['Software_Version'] = next(reader)[1]
            kwargs['Hardware_Revision'] = next(reader)[1]
            next(reader)#--------------
            next(reader)#Signal (ADV Values)
            kwargs['Maximum'] = np.int16(next(reader)[1])
            kwargs['Minimum'] = np.int16(next(reader)[1])
            kwargs['Meas_Range'] = next(reader)[1]
            kwargs['Step_Size'] = next(reader)[1]
            next(reader)#---------
            kwargs['Folder'] = next(reader)[1]
            #next(reader)#-----------
            #next(reader)#column labels
        return cls(**kwargs)
    def __iter__(self) -> Iterator[PL_Data_Row]:
        assert self._path is not None
        with PL_CSV_Reader(self._path,True) as reader:
            for line in reader:
                if(len(line)) < 3:
                    continue
                yield line_to_data(line)
    def __len__(self):
        assert self._path is not None
        if self._length is None:
            with open(self._path,'r') as f:
                self._length = sum(1 for _ in f)-NUMBER_ROWS_IN_HEADER
        return self._length