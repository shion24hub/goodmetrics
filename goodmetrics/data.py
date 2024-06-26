from dataclasses import dataclass

import numpy as np
import pandas as pd

@dataclass
class OHLCV:
    data: pd.DataFrame

    def __post_init__(self):

        # columns
        if 'datetime' != self.data.index.name:
            raise ValueError('`datetime` index not found in data')
        if 'open' not in self.data.columns:
            raise ValueError('`open` column not found in data')
        if 'high' not in self.data.columns:
            raise ValueError('`high` column not found in data')
        if 'low' not in self.data.columns:
            raise ValueError('`low` column not found in data')
        if 'close' not in self.data.columns:
            raise ValueError('`close` column not found in data')
        if 'volume' not in self.data.columns:
            raise ValueError('`volume` column not found in data')

        # dtype
        if self.data.index.dtype != 'datetime64[ns]':
            raise ValueError('`datetime` index not datetime64[ns]')
        if self.data['open'].dtype != np.float64:
            raise ValueError('`open` column not float64')
        if self.data['high'].dtype != np.float64:
            raise ValueError('`high` column not float64')
        if self.data['low'].dtype != np.float64:
            raise ValueError('`low` column not float64')
        if self.data['close'].dtype != np.float64:
            raise ValueError('`close` column not float64')
        if self.data['volume'].dtype != np.float64:
            raise ValueError('`volume` column not float64')