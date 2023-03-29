import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from .utils import StatSynonyms
from .stats import hitter_fwar, pitcher_fwar


# %%
def _drop_unneeded(df):
    """Clean an html tables to the essentials for spg estimation."""
    drops = [0, 1] if df.loc[1, 1] in ['BA', 'ERA'] else [0]
    out = (
        df
        .drop(drops, axis=0)
        .drop([0, 3], axis=1)
        .astype(float)
        .rename({1: 'stat', 2: 'points'}, axis=1)
    )
    return out

def _get_key(df) -> str:
    """Get the stat category used as a key in spg dict"""
    key = df.loc[1, 1] if df.loc[1, 1] in ['BA', 'ERA'] else df.loc[0, 1]
    return key.lower()

def slope_func(stat: pd.Series, points: pd.Series) -> float:
    """Function to get linear slope."""
    def slope(x, y): 
        return LinearRegression().fit(x, y).coef_[0, 0]
    def reshape(series):
        try:
            return series.to_numpy().reshape(-1, 1)
        except AttributeError:
            return series.reshape(-1, 1)
    return slope(reshape(stat), reshape(points))

def get_spg(df):
    key = _get_key(df)
    out = _drop_unneeded(df)
    slope = slope_func(out.stat, out.points)
    median = out.stat.median()
    return {key: {'spg': slope, 'median': median}}

# %%
def get_xspg(df) -> dict:
    """Get xstat from rate stat."""
    key = _get_key(df)
    df = _drop_unneeded(df)
    median = df.stat.median()
    if key == 'ba':   
        xh = 5600 * (df.stat - median)
        slope = slope_func(xh, df.points)
    if key == 'whip':
        xwhip = 1200 * (df.stat - median)
        slope = slope_func(xwhip, df.points)
    if key == 'era':
        xer = 1200 * (df.stat - median)
        slope = slope_func(xer, df.points)
    return {key: {'spg': slope, 'median': median}}


# %%
def get_spgs(dfs: list) -> dict:
    """Programmatically determine spgs."""
    spgs = {}
    for df in dfs:
        head = df.loc[1, 1] if df.loc[1, 1] in ['BA', 'ERA'] else df.loc[0, 1]
        if head.lower() not in ['ba', 'whip', 'era']:
            spg = get_spg(df)
        else:
            spg = get_xspg(df)
        spgs.update(spg)
    return spgs

# %%
def spgs_from_standings_html(path) -> pd.DataFrame:
    """Read an html of league standings and find spgs for categories.
    
    Notes:
        Rates stats are converted to expected counts based on an assumed 5600
        at bats or 1200 innings pitched. ERA is still on a 9 inning basis, so 
        reflects value per nine earned runs. This is for convenience:
            spg[era_9_run_basis] * IP * (ERA - lgERA) = fantansy_points
        
        Rate stats are calculated using the median value, not the mean, since 
        there are often extremes (saves punters, etc.) to skew the mean.
    """
    with open(path, 'r') as f:
        html = f.read()
    dfs = pd.read_html(html)
    return pd.DataFrame(get_spgs(dfs[1:])).T

class Valuator:
    def __init__(self, spg):
        self.spg = spg
        self.stat_syn = StatSynonyms()

    def clean_df(self, df, inplace=False) -> pd.DataFrame:
        """Clean df for processing."""
        if not inplace:
            df = df.copy()
            self.clean_df(df, inplace=True)
            return df
        df.rename(columns={k: self.stat_syn.normalize(k).lower() for k in df.columns}, inplace=True)

class ReplacementValuator(Valuator):
    positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']

    def valuate_hitters(self, df, depth) -> pd.Series:
        """Return the position-adjusted player value.

        For many league structures, this will return one number for catchers
        and another for all other players. This is because
        utility positions allow absorb most of the small gap between,
        e.g., second base and OF, so that the worst playable short stop
        is still better than the worst playable utility player.
        """
        df = self.clean_df(df)
        pos_values = self.find_position_values(df, depth)
        pos_values = {k: v for k, v in pos_values.items() if v != 0}
        pos_values = dict(sorted(pos_values.items(), key=lambda x: x[1], reverse=True))
        def best_pos_value(x):
            vals = [pos_values.get(pos, 0) for pos in x.split(',')]
            if not vals:
                return pos_values.get(x, 0)
            return max(vals)
        # TODO: reduce number of calls to hitter_fwar. There are a lot of them. 
        # this is a waste, but getting the job done ATM. 
        baseline_rep_level = hitter_fwar(df, self.spg).sort_values()[-depth:].values[0]
        x = df.eligible.apply(best_pos_value)
        return baseline_rep_level - x

    def valuate_pitchers(self, df, depth):
        df = self.clean_df(df)
        baseline_rep_level = pitcher_fwar(df, depth).sort_values()[-depth:][0]
        return baseline_rep_level
   
    def find_position_values(self, df, depth: int) -> dict:
        positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
        df = df.copy().rename(columns={k: k.lower() for k in df.columns})
        df['fwar'] = hitter_fwar(df, self.spg)
        df = df.sort_values('fwar', ascending=False)
        #print(df.head())
        raw_replace = df.fwar[:depth].values[-1]
        replace_values = {}
        for pos in self.positions:
            exp = f'{pos},|{pos}$'  # regex match postion followed by comma or EoL.
            _df = df[df.eligible.str.contains(exp)]
            replace_values[pos] = max(raw_replace - _df[:16].fwar.min(), 0)
        return replace_values


class FantasyValuator(Valuator):
    def __init__(self, spg):
        super().__init__(spg)
        self.replacement = ReplacementValuator(spg)

    def valuate_hitters(self, df, depth) -> pd.Series:
        fwar = self.hitter_fwar(df)
        replacement_level = self.replacement.valuate_hitters(df, depth)
        # print(replacement_level.min(), fwar.min())
        return fwar - replacement_level

    def valuate_pitchers(self, df, depth):
        fwar = self.pitcher_fwar(df)
        replacement_level = self.replacement_level(fwar, depth)
        return fwar - replacement_level

    def hitter_fwar(self, df) -> pd.Series:
        df = self.clean_df(df)
        return hitter_fwar(df, self.spg)

    def pitcher_fwar(self, df) -> pd.Series:
        df = self.clean_df(df)
        return pitcher_fwar(df, self.spg)

    def replacement_level(self, fwar: pd.Series, depth: int):
        return fwar.sort_values(ascending=False)[:depth].min()

class FantasyRateValuator(FantasyValuator):
    def valuate_pitchers(self, df, depth):
        df = self.clean_df(df)
        fwar = self.pitcher_fwar(df)
        ratio = 130 / df.ip
        for stat in ['k', 'w', 's']:
            df[stat] = ratio * df[stat]
        df.ip = 130
        return super().pitcher_fwar(df)

    def valuate_hitters(self, df, depth):
        df = self.clean_df(df)
        if not hasattr(df, 'pa'):
            df['pa'] = df.bb + df.ab
        ratio = 475 / df.pa
        for stat in ['hr', 'r', 'rbi', 'sb', 'ab']:
            df[stat] = df[stat] * ratio
        return super().hitter_fwar(df)



