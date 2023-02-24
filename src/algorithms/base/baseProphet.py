import os
import warnings
import seaborn as sbn
import mplfinance as mpf
import matplotlib.pyplot as plt
from algorithms.base.base import BaseAlgorithm

# We import the warnings library to stop warnings
# from showing up as they do not provide added insights
# into statistical analysis
warnings.filterwarnings('ignore')
sbn.set_style("whitegrid")


class BaseProphetAlgorithm(BaseAlgorithm):

    def start(self):
        pass

    def create_model(self, freq, new_model=True):
        pass

    def store_forecast(self, periods):
        pass

    def store_result(self, result: dict):
        pass

    def rename_model_columns(self, date_column="from_string", target_column="Close"):
        new_names = {
            date_column: "ds",
            target_column: "y",
        }
        self.model_dataset.rename(columns=new_names, inplace=True)

    def predict(self):
        return self.model.predict(self.future_dataset)

    def plot_data(self):
        current_directory = os.getcwd()
        path = "{}/images/{}".format(current_directory, self.__class__.__name__.lower())
        # Check whether the specified path exists or not
        exists = os.path.exists(path)
        if not exists:
            # Create a new directory because it does not exist
            os.makedirs(path)
        # Plot last 100 rows of our dataset
        mpf.plot(self.dataset.set_index("from_string").tail(100),
                 type="candle",
                 style="charles",
                 volume=True,
                 title="{} with interval of {} | Last 100 items".format(self.symbol,
                                                                        self.interval),
                 savefig="{}/overview_{}_{}.png".format(
                     path,
                     self.symbol.lower(),
                     self.interval),
                 figsize=(12, 7))

        # Show correlation between features!
        plt.figure(figsize=(15, 15))
        sbn.heatmap(self.dataset.corr(method="pearson"), annot=True, cmap="rainbow", linewidths=1, linecolor="black")
        plt.savefig("{}/correlation_{}_{}.png".format(
            path,
            self.symbol.lower(),
            self.interval), bbox_inches="tight", dpi=400)

    def plot_model(self):
        current_directory = os.getcwd()
        path = "{}/images/{}".format(current_directory, self.__class__.__name__.lower())
        # Check whether the specified path exists or not
        exists = os.path.exists(path)
        if not exists:
            # Create a new directory because it does not exist
            os.makedirs(path)
        fig1 = self.model.plot(self.forecast)
        fig1.savefig("{}/prices_{}_{}.png".format(
            path,
            self.symbol.lower(),
            self.interval), bbox_inches="tight")

        fig2 = self.model.plot_components(self.forecast)
        fig2.savefig("{}/components_{}_{}.png".format(
            path,
            self.symbol.lower(),
            self.interval), bbox_inches="tight")
