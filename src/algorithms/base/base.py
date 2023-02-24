import logging
import pandas as pd
from common.enums import KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_3MINUTE, KLINE_INTERVAL_5MINUTE, \
    KLINE_INTERVAL_15MINUTE, KLINE_INTERVAL_30MINUTE

class BaseAlgorithm:

    def __init__(self, symbol: str, interval:  str, dataset: pd.DataFrame) -> None:
        self.logger = logging.getLogger(__name__)
        self.symbol = symbol
        self.interval = interval
        self.model = None
        self.dataset = dataset
        self.model_dataset = None
        self.future_dataset = None
        self.forecast = None
        super().__init__()


    @staticmethod
    def future_periods() -> dict:
        # minutes_in_1_day = 1440 / 20160
        return {
            KLINE_INTERVAL_1MINUTE: {
                'periods': 30,  # 1 hour
                'freq': '1min',
            },
            KLINE_INTERVAL_3MINUTE: {
                'periods': 10,
                'freq': '3min',
            },
            KLINE_INTERVAL_5MINUTE: {
                'periods': 6,
                'freq': '5min',
            },
            KLINE_INTERVAL_15MINUTE: {
                'periods': 2,
                'freq': '15min',
            },
            KLINE_INTERVAL_30MINUTE: {
                'periods': 1,
                'freq': '30min',
            }
        }
