"""Functions for aligning datasets.

Contains functions for merging and combining data from diverse sources.
In order to work within a specific league but leverage data from other sources,
it's often necessary to merge datasets that don't share common fields.

"""

import warnings

from collections.abc import Callable, Iterable, Mapping


import pandas as pd
import numpy as np

from numpy.typing import ArrayLike
from scipy.stats import rankdata

from philosofool.data_sources.utils import read_yml  # type: ignore
from philosofool.data_science.graph import MetricGraph
from fantasy_baseball_draft.utils import StatSynonyms, load_cbs_data, DataLoader
from fantasy_baseball_draft.utils import cbs_player_col_to_df
from fantasy_baseball_draft.stats import StatCalculator



class AssociatePlayers:
    """Associate entities from different datasets.

    Given two dataframes that share entities but not a common single
    join key, this can construct a merge of the data based on columns
    that are assumed to find unique one.

    Example: Given dataframes of pitchers in 2019 that use different
    naming conventions ('Mike', 'Michael', etc.) we can align these by
    assuming that two pitchers are the same if they started the same
    number of games, had the same number of walks, hits and strikeouts.
    """
    synonyms = StatSynonyms()

    def associate(self, df1: pd.DataFrame, df2: pd.DataFrame, index_cols: list) -> pd.DataFrame:
        if df1.duplicated().sum():
            warnings.warn("Found duplicated in df1.")
        if df2.duplicated().sum():
            warnings.warn("Found duplicated in df2.")
        df1 = self.synonyms.normalize_df(df1)
        df2 = self.synonyms.normalize_df(df2)
        df = df1.set_index(index_cols).merge(df2.set_index(index_cols), left_index=True, right_index=True)
        return df


def merge_on_name(cbs: pd.DataFrame, fg: pd.DataFrame) -> pd.DataFrame:
    cbs_player = (
        cbs_player_col_to_df(cbs.Player)
        .merge(cbs[['Player']], left_index=True, right_index=True)
        .merge(fg[['Name', 'playerid']], on='Name', how='left')
    )
    return cbs_player


def map_cbs_player_col_to_id_by_name(cbs: pd.DataFrame, fg: pd.DataFrame) -> pd.Series:
    """Use cbs "Player" field to return series of CBS player names to fg player ids."""
    df = merge_on_name(cbs, fg).drop_duplicates(subset=['playerid'], keep=False)
    ids = df.set_index('Player').playerid.dropna().astype(str)
    return ids.where(ids.str.startswith('sa'), ids.str.strip('sa').astype(int))


def build_id_map(df: pd.DataFrame, fg_df: pd.DataFrame, ids: pd.Series) -> pd.Series:
    """Map cbs Player column to fg ids.

    Parameters
    ----------
    df:
        CBS data.
    fg_df:
        Fangraphs data.
    ids:
        Mapping of Player:fg_id; this is a mapping of known cases.
    """
    df = df.copy()
    df['playerid'] = df.Player.map(ids).fillna(-1)
    name_ids = map_cbs_player_col_to_id_by_name(df[df.playerid == -1], fg_df)
    name_ids = name_ids[~name_ids.duplicated()]
    ids = pd.concat([ids, name_ids]).to_dict()
    return df.Player.map(ids).fillna(-1)


def build_id_map_from_stat_associations(cbs: pd.DataFrame, fg: pd.DataFrame, index_cols: list[str], duplicated=False) -> pd.Series:
    """Return series mapping CBS player "Player" column to a fangraphs ID column."""
    cbs_with_playtime = cbs[cbs[index_cols].sum(axis=1) > 0]
    n_players_with_pt = len(cbs_with_playtime)
    # TODO: this is gross multipurpose function. Fix your 2022 mistakes!
    if duplicated:
        return cbs_with_playtime[cbs_with_playtime.duplicated(subset=index_cols, keep=False)]
    cbs_with_playtime = cbs_with_playtime.drop_duplicates(subset=index_cols, keep=False)
    # eww. Side effects.
    print(f"Dropped {n_players_with_pt - len(cbs_with_playtime)} duplicated records.")

    cbs_to_fg = AssociatePlayers().associate(cbs_with_playtime, fg, index_cols)
    cbs_to_fg.Player = cbs_to_fg.Player.str.strip()
    as_dict = dict(zip(cbs_to_fg.Player.str.strip(), cbs_to_fg.playerid))
    return pd.Series(as_dict)
