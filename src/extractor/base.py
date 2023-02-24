import os
import logging
from pathlib import Path


class BaseExtractor:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__()

    def check_or_create_path(self):
        current_directory = os.getcwd()
        path = "{}/data/{}".format(current_directory, self.__class__.__name__.lower())
        # Check whether the specified path exists or not
        exists = os.path.exists(path)
        if not exists:
            # Create a new directory because it does not exist
            os.makedirs(path)
        return path

    @staticmethod
    def file_exists(path, symbol, interval):
        path_to_file = "{}/{}_{}.csv".format(path,
                                             symbol.lower(),
                                             interval)
        path = Path(path_to_file)
        if path.is_file():
            return True, path_to_file
        else:
            return False, path_to_file

    @staticmethod
    def interval_to_seconds(interval: str) -> int:
        """Convert a Binance interval string to milliseconds
        :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
        :type interval: str
        :return:
             None if unit not one of m, h, d or w
             None if string not in correct format
             int value of interval in milliseconds
        """
        seconds = None
        seconds_per_unit = {
            "m": 60,
            "h": 60 * 60,
            "d": 24 * 60 * 60,
            "w": 7 * 24 * 60 * 60,
            "s": 1,
        }

        unit = interval[-1]
        if unit in seconds_per_unit:
            try:
                seconds = int(interval[:-1]) * seconds_per_unit[unit]
            except ValueError:
                pass
        return seconds
