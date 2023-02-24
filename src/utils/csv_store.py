import os
from typing import Optional, Union

import pandas as pd
from pandas import DataFrame


class CSVStore:

    @classmethod
    def store(cls, dataframe: pd.DataFrame, filename='store.csv', iteration=0):
        with open('{0}'.format(filename), 'w', encoding='utf-8') as outfile:
            if iteration == 0:
                header_show = True
                iteration += 1
            else:
                header_show = False
            dataframe.to_csv('{0}'.format(filename),
                             index=True, index_label='index', mode='a', header=header_show)

    @classmethod
    def read(cls, filename='store.csv') -> Union[Optional[DataFrame], Optional[None]]:
        if os.path.exists('{0}'.format(filename)) and os.path.getsize(
                '{0}'.format(filename)) > 0:
            with open('{0}'.format(filename), 'rU') as outfile:
                return pd.read_csv(outfile, delimiter=",", index_col="index", parse_dates=True)
        else:
            return None

    @classmethod
    def last_obj(cls, based_on: str, filename='store.csv'):
        old_objs = CSVStore.read(filename)
        if old_objs is not None and len(old_objs.index) >= 1:
            return old_objs, old_objs[based_on].iloc[-1]
        return None, None
