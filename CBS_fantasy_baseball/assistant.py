import pandas as pd
import numpy as np
import stats

class FantasyBaseballAssistant:
    def __init__(self, league_data, advanced_data):
        self.league_data = league_data
        self.advanced_data = advanced_data
        self.stat_calculator = stats.StatCalculator()




