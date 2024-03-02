"""Handle stats."""

from collections.abc import Callable, Iterable, Hashable, Mapping  # noqa: F401  ignore stale import
from typing import Any, Optional  # noqa: F401  ignore stale import
import functools
import re
import warnings

import pandas as pd
import numpy as np
from numpy.typing import ArrayLike

from philosofool.functional.functional import compose_function
from philosofool.data_science.graph import MetricGraph


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


class Graph(MetricGraph):
    """Provide calculations for baseball stats.

    Following conventions used in other data science packages, we use the term "metric"
    for a stat. ERA is a "metric".

    Follows standard graphlib conventions: a graph is a mapping from Hashable elements to
    a Hashable sequence.

    The model of metrics is a mapping of metrics to callables and metrics to dependencies.
    The class handles the calculation of metrics in a Pandas dataframe.

    Follows standard graphlib conventions: a graph is a mapping from Hashable elements to
    a Hashable sequence.

    Attributes
    ----------
        dependency_graph
            The model of dependency: A mapping from hashable values to a sequence of hashable values.
        metric_functions
            Mapping of metrics from the graph to functions that calculate them.

            This assumes that the ordering of dependencies corresponds to the order in the dependency graph.

    Class Methods
    -------------
        from_model:
           Construct an instance from a model: a mapping from names to a pair of a function and a dependency list.

    Methods
    -------
        calculate_metrics:
           Compute the metrics from a DataFrame.
        add_metrics:
            Add metric calculations to a DataFrame.
        get_metric_dependencies:
            Find all metrics required to compute a metric.
    """

    @staticmethod
    def reduce_sum(*args):
        return functools.reduce(np.add, args)

    model = {
        'H': (reduce_sum, ('1B', '2B', '3B', 'HR')),
        'TB': (
            compose_function(
                lambda args: np.stack(args, axis=1),
                lambda bases: np.sum(bases * np.array([1, 2, 3, 4]), axis=1)
            ),
            ('1B', '2B', '3B', 'HR')
         ),
        'AB': (reduce_sum, ('PA', 'BB')),
        'BA': (np.divide, ('H', 'AB')),
        'SLG': (np.divide, ('TB', 'AB')),
        'TOB': (np.add, ('BB', 'H')),  # Times on Base
        'OBP': (np.divide, ('TOB', 'PA')),
        'OPS': (np.add, ('OBP', 'SLG')),
        'WHIP': (np.divide, ('TOB', 'IP')),
        'ERA': (lambda er, ip: (er / ip) / 9, ('ER', 'IP')),
        'BIP': (lambda ab, hr, k: ab - (hr + k), ('AB', 'HR', 'K')),
        'BABIP': (lambda bip, h, hr, ab: ((h - hr) / bip), ('BIP', 'H', 'HR')),
    }

    dependency_graph: dict[str, tuple[str, ...]] = {key: dependencies for key, (_, dependencies) in model.items()}
    metric_functions: dict[str, Callable[..., ArrayLike]] = {key: fn for key, (fn, _) in model.items()}

    def __init__(self, graph_update: Optional[dict] = None, metrics_update: Optional[dict] = None):
        match graph_update, metrics_update:
            case None, None:
                pass
            case dict() as graph, dict() as metrics:
                if set(graph).intersection(metrics) != set(graph):
                    raise ValueError("graph_update and metric_update are disjoint.")
                if len(graph) != len(metrics):
                    warnings.warn("Metrics functions includes some ungraphed dependencies.")
                self.dependency_graph.update(graph_update)
                self.metric_functions.update(metrics_update)
            case _, _:
                raise Exception("You must provide both metrics and a graph when updating.")

def pitcher_fwar(pitcher: pd.DataFrame, spg: pd.Series) -> pd.Series:
    """Return pitcher spg weighted values."""
    league = spg['median']
    spg = spg['spg']
    fwar = (
        pitcher.k * spg['k']
        + pitcher.w * spg['w']
        + pitcher.s * spg['s']
        + ((pitcher.era - league['era']) / 9 * pitcher.ip * spg['era']).fillna(0)
        + ((pitcher.whip - league['whip']) * pitcher.ip * spg['whip']).fillna(0)
    )
    return fwar


def hitter_fwar(hitter: pd.DataFrame, spg: pd.Series) -> pd.Series:
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