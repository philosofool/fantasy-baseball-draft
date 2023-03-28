"""Handle stats."""

import pandas as pd

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