from collections.abc import Callable
import pandas as pd
import os

from pybaseball import statcast, playerid_lookup, playerid_reverse_lookup

class FetchStatcast:
    """Fetch Statcast data.

    Reads from and writes to caches during fetches by default, preventing needless
    API calls and speeding up transactions.
    """

    def __init__(self, local_file_cache: str):
        self.local_file_cache = local_file_cache

    def statcast(
            self,
            start: str,
            end: str,
            preprocess: Callable[[pd.DataFrame], pd.DataFrame],
            read_from_cache=True,
            write_to_cache=True
        ) -> pd.DataFrame:
        """Fetch pitch level data from statcast.

        Data is read from local_file_cache.

        Parameters
        ----------
        start:
            YYYY-MM-DD formatted time string.
        end:
            YYYY-MM-DD formatted time string.
        preprocess:
            A callable for transforming slices of statcast data.

            The fetch process works on one-day chunks of statcast data. This function is called on each
            chunk before aggragating all the data.
        read_from_cache:
            Whether to read from local_file_cache if available.
        write_to_cache:
            Whether to write fetched data to cache.
        """
        dates = pd.date_range(start, end)
        data = []
        for _start, _end in zip(dates, dates[1:]):
            df = self._fetch_data(_start, _end, read_from_cache, write_to_cache)
            data.append(preprocess(df))
        return pd.concat(data)

    def _fetch_data(self, start: pd.Timestamp, end: pd.Timestamp, use_cache: bool, write_to_cache: bool):
        """Fetch a single slice of data through a cache file."""
        filename = self._file_name(start, end)
        if os.path.exists(filename) and use_cache:
            df = pd.read_parquet(filename)
        else:
            start_str = start.strftime("%Y-%m-%d")
            end_str = end.strftime("%Y-%m-%d")
            df = statcast(start_str, end_str)
            if write_to_cache:
                df.to_parquet(filename)
        return df

    def _file_name(self, start: pd.Timestamp, end: pd.Timestamp):
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        name = f"statcast_{start_str}_{end_str}"
        return os.path.join(self.local_file_cache, name)