from collections.abc import Callable, Iterable
from functools import partial
import pandas as pd
import numpy as np
from scipy.stats import rankdata
from numpy.typing import ArrayLike
from sklearn.linear_model import LinearRegression

from .utils import StatSynonyms
from .stats import hitter_fwar, pitcher_fwar

from philosofool.data_science.graph import MetricGraph


def weighted_ratio(x: ArrayLike, weight: ArrayLike, median: ArrayLike):
    return weight * (x - median)

def model_spg(arr: np.ndarray|pd.Series, low_better=False) -> Callable[[ArrayLike], np.ndarray]:
    """Calculate a linear regression for spg weights and return a function that applies it."""
    if isinstance(arr, pd.Series):
        arr = arr.values
    arr = arr.reshape(-1, 1)
    points = rankdata(arr * -1) if low_better else rankdata(arr)
    slope = LinearRegression().fit(arr, points).coef_[0]

    def spg_value(x: ArrayLike) -> np.ndarray:
        return x * slope

    return spg_value


spg_model = MetricGraph.from_model({
    # 'IP': (lambda _: 1200., ('ERA',)),
    # 'AB': (lambda _: 5600., ('BA',)),
    'median_ERA': (np.median, ('ERA',)),
    'median_WHIP': (np.median, ('WHIP',)),
    'median_BA': (np.median, ('BA',)),
    'xER': (weighted_ratio, ('ERA', 'IP', 'median_ERA')),
    'xWHIP': (weighted_ratio, ('WHIP', 'IP', 'median_WHIP')),
    'xH': (weighted_ratio, ('BA', 'AB', 'median_BA')),
    'W_spg': (model_spg, ('W',)),
    'S_spg': (model_spg, ('S',)),
    'K_spg': (model_spg, ('K',)),
    'ERA_spg': (partial(model_spg, low_better=True), ('xER',)),
    'WHIP_spg': (partial(model_spg, low_better=True), ('xWHIP',)),
    'R_spg': (model_spg, ('R',)),
    'HR_spg': (model_spg, ('HR',)),
    'RBI_spg': (model_spg, ('RBI',)),
    'SB_spg': (model_spg, ('SB',)),
    'BA_spg': (model_spg, ('xH',)),
})

# Positional eligibilty and positional value

def largest(arr: np.ndarray, k: int) -> np.ndarray:
    """Return the k largest elements in an array.

    The output is unsorted, but element 0 is its minimum value.
    """
    k_ = arr.size - k
    return np.partition(arr, kth=k_)[-k:]

def position_value(hitter_fwar: ArrayLike, eligible: ArrayLike, position: str, n_rostered: int) -> float:
    if hasattr(hitter_fwar, 'values') :
        hitter_fwar = hitter_fwar.values
    eligible_idx = np.nonzero(matches_eligible(eligible, position))
    best = np.partition(hitter_fwar[eligible_idx], kth=n_rostered)[-n_rostered:]
    return best[0]

def matches_eligible(eligbible: ArrayLike, position: str) -> pd.Series:
    """Return boolean series where eligible matches position."""
    elig_series = pd.Series(eligbible)
    pattern = f'^{position}$|,{position},|^{position},|,{position}$'
    clean_elig = elig_series.str.replace(r'\s', '', regex=True)
    return clean_elig.str.contains(pattern, regex=True)


def position_adjusted_fwar(raw_fwar: ArrayLike, eligible: ArrayLike, position: str, pos_rostered: int, roster_depth: int) -> np.ndarray:
    """Model position adjusted fantasy value."""
    # TODO: Figure out how to link graphs so that positional valuation can pass through more efficiently:
    # this process won't cache positional value during the calculations, so multiple calls repeat the
    # baseline call.
    raw_fwar = raw_fwar.fillna(-1.)
    baseline_replacement_level = largest(raw_fwar, roster_depth)[0]
    position_replacement_level = position_value(raw_fwar, eligible, position, pos_rostered)
    pos_value = baseline_replacement_level - position_replacement_level
    return np.where(matches_eligible(eligible, position), raw_fwar + pos_value - baseline_replacement_level, raw_fwar - baseline_replacement_level)


# some tests

def test_matches_eligible():
    """Test of matches_eligible."""
    eligible = ['C', 'C, CF', '1B, C', '1B, C, SS', 'CF', 'SS']
    result = matches_eligible(eligible, 'C')
    assert np.array_equal(result, [True, True, True, True, False, False])

def test_postion_value():
    """Test of postiion_values."""
    fwar = np.arange(11, 0, -1) + 2
    eligible = np.array(('c' + ' 1b'*6 + ' c'*4).split())
    result = position_value(fwar, eligible, 'c', 4)
    assert result == 3
    result = position_value(fwar, eligible, 'c', 1)
    assert result == 13
    np.testing.assert_raises(ValueError, position_value, fwar, eligible, 'c', 10)

    fwar = pd.Series(fwar)  # series may not play with internals of position_value.
    result = position_value(fwar, eligible, 'c', 4)
    assert result == 3

if __name__ == '__main__':
    test_matches_eligible()
    test_postion_value()