"""
Utilties for fantasy baseball.
"""


import pandas as pd
import os

from philosofool.data_science.clean import Concordance

class DataLoader:

    def __init__(self, directory):
        self.dir = directory
        self.synonyms = StatSynonyms()

    def load_csv(self, name):
        path = os.path.join(self.dir, name)
        df = pd.read_csv(path)
        return self.synonyms.normalize_df(df)

    def load_cbs_csv(self, name):
        path = os.path.join(self.dir, name)
        df = load_cbs_data(path)
        return self.synonyms.normalize_df(df)


def load_cbs_data(path) -> pd.DataFrame:
    """Load cleaned cbs projections."""
    path = os.path.normpath(path)
    df = pd.read_csv(path, skiprows=1, skipfooter=1, engine='python')
    df = df[[col for col in df.columns if 'Unnamed' not in col]]
    df.Player = df.Player.str.strip()
    return df

def cbs_player_col_to_df(player: pd.Series) -> pd.DataFrame:
    """Transform Player column to a DataFrame."""
    name_re = "(.+) ([123]B|\w{1,2}) \|\s(\w{2,3})"
    groups = ['Name', 'Pos', 'Team']
    return (
        player.str.extract(name_re)
        .rename(columns={i: group for i, group in enumerate(groups)})
        .set_index(player.index)
    )

class StatSynonyms(Concordance):
    """Concordance of stat synonyms used in baseball.

    Example usage:
        stat_synonyms = StatSynonyms()
        assert stat_synonyms.normalize('SO') == 'K'
    """
    def __init__(self):
        ...
        self.syn_set = {
            'AVG': 'BA',
            'INN': 'IP',
            'INNS': 'IP',
            'BBI': 'BB',
            'SO': 'K',
            'SV': 'S',
            'APP': 'G',
            'PLAYERID': 'playerid'
        }

    def normalize(self, abbr):
        return self.syn_set.get(self.preprocess(abbr), abbr)

    def preprocess(self, value):
        return value.replace('.', '').upper()

    def normalize_df(self, df, inplace=False):
        """Normalize dataframe column names."""
        if not inplace:
            df = df.copy()
            self.normalize_df(df, True)
            return df
        df.rename(columns={k: self.normalize(k) for k in df.columns}, inplace=True)
