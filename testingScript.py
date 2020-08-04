# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 06:15:46 2019

@author: lenha
"""

import pandas as pd

from CBS_fantasy_baseball.stats import StatCalculator

def test_StatCalculator():
    calc = StatCalculator()
    jackie = {'HR': 12, 'RBI': 48,'R': 120, 'SB': 29, 'AB': 590, 'H': 175, 'BA': 175/590, 'hr': 12}
    stat_dict = {'HR': 'HR', 'RBI': 'RBI','R': 'R', 'SB': 'SB', 'AB': 'AB', 'H': 'H', 'BA': 'BA', 'hr': 'HR'}
    calc.hitterFWAR(jackie)
    calc.hitterFWAR(jackie, use_count_stats = False, stat_dict=stat_dict)
    satchel = {'K': 43,'IP': 72.2, 'BB': 22, 'H': 61, 'WHIP': (61+22)/72.2, 'ER': 20, 'ERA': 2.48, 'SV': 1, 'S': 1, 'W': 6}
    calc.pitcherFWAR(satchel)
    calc.pitcherFWAR(satchel, use_count_stats=False)
    satchel.pop('K')
    satchel['SO'] = 43
    calc.pitcherFWAR(satchel, stat_dict = {'K':'SO'})


test_StatCalculator()