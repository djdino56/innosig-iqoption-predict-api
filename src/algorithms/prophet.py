import os
import json
import numpy as np
from pathlib import Path
import datetime as datetime

from database.models.model_result import ModelResult
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from algorithms.base.baseProphet import BaseProphetAlgorithm


class ProphetAlgorithm(BaseProphetAlgorithm):

    def store_forecast(self, periods):
        sliced_rows = json.loads(self.forecast.iloc[-periods:].to_json(orient="records", date_format='iso'))
        results = []
        for slice_row in sliced_rows:
            result = {
                "algorithm": self.__class__.__name__.lower(),
                "market": self.symbol,
                "interval": self.interval,
                "date": datetime.datetime.strptime(slice_row["ds"], "%Y-%m-%dT%H:%M:%S.%f"),
                "price": slice_row["yhat"]
            }
            ProphetAlgorithm.store_result(result)
            self.logger.info(result)
            results.append(result)
        return results

    def create_model(self, freq, new_model=True):
        current_directory = os.getcwd()
        path_to_file = "{}/models/model_{}_{}_{}.json".format(current_directory,
                                                              self.__class__.__name__.lower(),
                                                              self.symbol.lower(),
                                                              self.interval)
        # path = Path(path_to_file)
        # if path.is_file() and not new_model:
        #     self.logger.info(f'The file {path_to_file} exists')
        #     with open(path_to_file, 'r') as fin:
        #         return model_from_json(fin.read())
        # else:
        # self.logger.info(f'The file {path_to_file} does not exist')
        self.logger.info('Creating model of {}'.format(self.__class__.__name__.lower()))
        # with open(path_to_file, 'w') as fout:
        m = Prophet(
            yearly_seasonality=False,
            daily_seasonality=False,
            weekly_seasonality=False
        )
        m.fit(self.model_dataset)  # TODO: freq unused
        # fout.write(model_to_json(m))  # Save model
        return m

    def start(self):
        # Plot the dataset
        self.plot_data()
        # Slice target columns from original dataset
        self.model_dataset = self.dataset[["close_time_string", "Close"]]
        # Rename columns for model
        self.rename_model_columns()
        # Get periods and freq
        periods = self.future_periods()[self.interval]['periods']
        freq = self.future_periods()[self.interval]['freq']

        # Load model
        self.model = self.create_model(freq)
        # Create future dataset
        self.future_dataset = self.model.make_future_dataframe(periods=periods, freq=freq)
        # Forecast future dataset
        self.forecast = self.predict()
        # self.logger.info(self.forecast[['ds', 'yhat1']].tail(periods))
        self.plot_model()
        self.store_forecast(periods)
