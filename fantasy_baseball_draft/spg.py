import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


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
    

# %%



