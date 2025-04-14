import csv
import os

ENCODING = 'utf_16_le'
DIALECT = 'excel-tab'
NUMBER_ROWS_IN_HEADER = 16

class PL_CSV_Reader:
    def __init__(self,path:str|os.PathLike,skip_header:bool = False):
        self._path = path
        self._skip_header = skip_header
    def __enter__(self):
        self._file = open(self._path,'r',encoding=ENCODING)
        reader = csv.reader(self._file,dialect=DIALECT)
        if self._skip_header:
            for _ in range(NUMBER_ROWS_IN_HEADER):
                next(reader)
        return reader
    def __exit__(self,*args):
        self._file.close()