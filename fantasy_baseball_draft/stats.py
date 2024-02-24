"""Handle stats."""

import pandas as pd
import numpy as np
from numpy.typing import ArrayLike


class StatSynonyms:
    """Concordance of stat synonyms used in baseball.

    Example usage:
        stat_synonyms = StatSynonyms()
        assert stat_synonyms.normalize('SO') == 'K'
    """
    def __init__(self):
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

    def normalize(self, abbr: str) -> str:
        return self.syn_set.get(self.preprocess(abbr), abbr)

    def preprocess(self, value):
        return value.replace('.', '').upper()

    def normalize_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize dataframe column names."""
        df = df.copy()
        return df.rename(columns={k: self.normalize(k) for k in df.columns})


def pitcher_fwar(pitcher: pd.DataFrame, spg: pd.DataFrame) -> pd.Series:
    """Return pitcher spg weighted values."""
    league = spg['median']
    spg = spg['spg']
    fwar = (
        pitcher.k * spg['k']
        + pitcher.w * spg['w']
        + pitcher.s * spg['s']
        + ((pitcher.era - league['era'])/9 * pitcher.ip * spg['era']).fillna(0)
        + ((pitcher.whip - league['whip']) * pitcher.ip * spg['whip']).fillna(0)
    )
    return fwar

def hitter_fwar(hitter: pd.DataFrame, spg: pd.DataFrame) -> pd.Series:
    """Return hitter spg weighted values."""
    league = spg['median']
    spg = spg.spg
    ba = hitter.h / hitter.ab
    fwar = (
        hitter.r * spg['r']
        + hitter.hr * spg['hr']
        + hitter.rbi * spg['rbi']
        + hitter.sb * spg['sb']
        + ((ba - league['ba']) * hitter.ab * spg['ba']).fillna(0)
    )
    return fwar