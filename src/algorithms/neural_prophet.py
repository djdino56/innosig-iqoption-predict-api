import os
import json
import datetime as datetime
from algorithms.base.baseProphet import BaseProphetAlgorithm
from pathlib import Path
from neuralprophet import NeuralProphet, save, load

from database.models.model_result import ModelResult


class NeuralProphetAlgorithm(BaseProphetAlgorithm):

    def store_forecast(self, periods, mgr=None, store_in_db=False):
        sliced_rows = json.loads(self.forecast.iloc[-periods:].to_json(orient="records", date_format='iso'))
        results = []
        for slice_row in sliced_rows:
            result = {
                "a": self.__class__.__name__.lower(),
                "m": self.symbol,
                "i": self.interval,
                # "d": datetime.datetime.strptime(slice_row["ds"], "%Y-%m-%dT%H:%M:%S.%f"),
                "d": slice_row["ds"],
                "p": slice_row["yhat1"]
            }
            if store_in_db:
                NeuralProphetAlgorithm.store_result(result)
            elif mgr is not None:
                mgr.emit('ALGO_UPDATE', data=result)
            self.logger.info(result)
            results.append(result)
        return results
        # from database.models.candle import Candle
        # found_candle, candle = Candle.find_by_date(slice_row["date"], self.symbol, self.interval)
        # if not found_candle:
        #     candle = Candle(**slice_row)
        #     candle.save()

    def create_model(self, freq, new_model=True):
        current_directory = os.getcwd()
        path_to_file = "{}/models/model_{}_{}_{}.np".format(current_directory,
                                                            self.__class__.__name__.lower(),
                                                            self.symbol.lower(),
                                                            self.interval)
        # path = Path(path_to_file)
        # if path.is_file() and not new_model:
        #     self.logger.info(f'The file {path_to_file} exists')
        #     return load(path_to_file)
        # else:
        #     self.logger.info(f'The file {path_to_file} does not exist')
        m = NeuralProphet(
            yearly_seasonality=False,
            daily_seasonality=False,
            weekly_seasonality=False
        )
        m.fit(self.model_dataset, freq=freq)
        # save(m, path_to_file)
        return m

    def start(self, mgr=None):
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
        self.future_dataset = self.model.make_future_dataframe(df=self.model_dataset, periods=periods,
                                                               n_historic_predictions=len(self.model_dataset))
        # Forecast future dataset
        self.forecast = self.predict()
        # self.logger.info(self.forecast[['ds', 'yhat1']].tail(periods))
        self.plot_model()
        return self.store_forecast(periods, mgr)
