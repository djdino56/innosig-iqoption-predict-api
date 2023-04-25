import numpy as np
import pandas as pd

from exchanges.singletons.binance_client_singleton import BinanceClientSingleton
from extractor.base import BaseExtractor
from settings import DEFAULT_TIME_PERIOD
from utils.csv_store import CSVStore


class BinanceExtractor(BaseExtractor):

    def __init__(self) -> None:
        self.exchange = BinanceClientSingleton.instance()
        super().__init__()

    def connect(self):
        self.logger.info("=======================")
        self.logger.info("Starting socket servers...")
        self.logger.info("=======================")

    def retrieve(self, symbol, interval, reset_index=True):
        path = self.check_or_create_path()
        results = self.exchange.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=DEFAULT_TIME_PERIOD
        )
        return self.preprocessing(results, path, symbol, interval, reset_index)

    def preprocessing(self, results, path, symbol, interval, reset_index=True):
        dataset = pd.DataFrame(results,
                               columns=["open_time",
                                        "Open",
                                        "High",
                                        "Low",
                                        "Close",
                                        "Volume",
                                        "close_time",
                                        "qav",
                                        "num_trades",
                                        "taker_base_vol",
                                        "taker_quote_vol",
                                        "ignore"])
        # Store raw data or fill raw data with new data
        check_file, filename = self.file_exists(path, symbol, interval)
        if not check_file:
            # Reset index of dataframe
            dataset.reset_index(inplace=True, drop=True)
            CSVStore.store(dataset, filename)
        else:
            old_dataframe, last_date = CSVStore.last_obj('close_time', filename)
            new_dataframe = dataset.loc[dataset['close_time'] > last_date]
            dataset = pd.concat([old_dataframe, new_dataframe])
            # Reset index of dataframe
            dataset.reset_index(inplace=True, drop=True)
            CSVStore.store(dataset, filename)

        # Print amount of datapoints
        amount_of_datapoints = len(dataset['Close'])
        self.logger.info("The dataset contains {} datapoints".format(amount_of_datapoints))

        # Convert datetime epoch to string
        for col in ['open_time', 'close_time']:
            date_col = pd.to_datetime(dataset[col], unit='ms')
            # else:
            #     date_col = pd.to_datetime(dataset[col], unit='ms')
            # date_col = date_col.dt.tz_localize(timezone.utc)
            # date_col = date_col.dt.tz_convert(pytz.timezone('Europe/Amsterdam'))
            dataset[col + '_string'] = date_col
            # dataset[col + '_hour'] = date_col.dt.hour
            # dataset[col + '_hour'] = date_col.dt.hour
            # dataset[col + '_minute'] = date_col.dt.minute
            # dataset[col + '_second'] = date_col.dt.second
            # dataset[col + '_day'] = date_col.dt.day
            # dataset[col + '_month'] = date_col.dt.month
            # dataset[col + '_year'] = date_col.dt.year

        # Convert string to floats
        dataset['Open'] = dataset['Open'].astype(np.float64)
        dataset['Close'] = dataset['Close'].astype(np.float64)
        dataset['Low'] = dataset['Low'].astype(np.float64)
        dataset['High'] = dataset['High'].astype(np.float64)
        dataset['Volume'] = dataset['Volume'].astype(np.float64)

        # Drop Volume being 0
        no_volume = dataset[dataset["Volume"] == 0].index
        data = dataset.drop(no_volume, axis=0)
        self.logger.info("{} rows were dropped because there was a value of 0 for volume".format(len(no_volume)))

        # Print Shape
        self.logger.debug(dataset.shape)
        # Print top of the dataframe
        self.logger.debug(dataset.head())
        # Print missing value per column
        for key in dataset.keys():
            self.logger.info(" {0} : {1} missing value(s)".format(key, data[key].isna().sum()))
        return dataset
