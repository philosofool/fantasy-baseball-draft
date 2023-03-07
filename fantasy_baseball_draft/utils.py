"""
Utilties for fantasy baseball.

Functions

    load_cbs_data: load data, dropping default header, footer and "Unnamed: 0" cols.
    
    process_players: columns to lower case, add columns for name, team, drop "player"
    
    process hitters: adds eligibility.
"""


import pandas as pd
import os

from philosofool.data_science.clean import Concordance

# very generic

def load_cbs_data(path) -> pd.DataFrame:
    """Load cleaned cbs projections."""
    path = os.path.normpath(path)
    df = pd.read_csv(path, skiprows=1, skipfooter=1, engine='python')
    df = df[[col for col in df.columns if 'Unnamed' not in col]]
    return df

def process_players(players: pd.DataFrame) -> pd.DataFrame:
    """Process player data."""
    players = players.rename({col: col.lower() for col in players.columns}, axis=1)
    players['name'] = players.player.apply(lambda x: process_cbs_player(x)[0])
    players['team'] = players.player.apply(lambda x: process_cbs_player(x)[1])
    first_cols = ['avail', 'name', 'team']
    players = players[first_cols + [col for col in players.columns if col not in first_cols]]#.drop('player', axis=1)
    return players

def process_hitters(hitters, hitter_elig):
    """Add Eligibility for players."""
    hitters = hitters.merge(hitter_elig[['Player', 'Eligible']], how='left', on='Player')
    hitters = process_players(hitters)
    #hitters['name'] = hitters.player.split("|")[0]
    return hitters

def process_cbs_player(player) -> tuple:
    """Process the fucking stupid "Player" column in CBS data."""
    split = player.split("|")
    name = " ".join(split[0].strip().split(' ')[:-1])
    team = split[1].strip()
    return name, team

def free_agents(players: pd.DataFrame) -> pd.DataFrame:
    """Filter non-free agents from dataframe."""
    fa_expression = r"(W(\s?)\()|(FA)"
    return players.avail.str.match(fa_expression)


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
            'INNs': 'IP',
            'BBI': 'BB',
            'SO': 'K',
            'SV': 'S'
        }
        
    
    def preprocess(self, value):
        return value.remove('.').upper()




