# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:35:31 2017

This is for creating lists of fangraphs players based on their inclusion in a CBSFile of KLF teams.


@author: lenhart
"""

from BaseClasses.BaseFantasyClasses import Pitcher
from BaseClasses.BaseFantasyClasses import Hitter
from BaseClasses.BaseFantasyClasses import SimplePlayer
from BaseClasses.BaseFantasyClasses import CBSFilePlayers
from BaseClasses.BaseFantasyClasses import HitterFile
from BaseClasses.BaseFantasyClasses import DepthPitcherFile
##from BaseClasses.BaseFantasyClasses import PitcherFile

import csv

def test():##a script for testing
    players = PlayerExtractor("Files/FGDepthProjHitters2017-3-20.csv","Files/FGDepthProjPitchers2017-3-20.csv","Files/CBSHitters.csv","Files/CBSPitchers.csv")
    ##players = PlayerExtractor("Files/testHitters.csv","Files/testPitchers.csv","Files/CBSHitters.csv","Files/CBSPitchers.csv")
    print(players.teamsInCBS())
    print(type(players.hittersOnTeam("Omak W...")[0]))
    print(players.pitchersOnTeam("Omak W..."))

    
class PlayerExtractor:
    def __init__(self,FGHitters,FGPitchers,CBSHitters,CBSPitchers):
        self.FGHittersFile = csv.DictReader(FGHitters)
        self.FGPitchersFile = csv.DictReader(FGPitchers)
        self.CBSHittersFile = csv.DictReader(CBSHitters)
        self.CBSPitchersFile = csv.DictReader(CBSPitchers)
        
        self.FGHitters = HitterFile(FGHitters)
        self.FGPitchers = DepthPitcherFile(FGPitchers)
        self.CBSHitters = CBSFilePlayers(CBSHitters)
        self.CBSPitchers = CBSFilePlayers(CBSPitchers)

        self.assignEligibilities()
        
    def teamsInCBS(self):
        out = []
        for guy in self.CBSHitters:
            if guy.avail not in out:
                out.append(guy.avail)
        return out
    
    def hittersOnTeam(self,team):
        out = []
        for guy in self.CBSHitters.listOfGuysOnTeam(team):
            for dude in self.FGHitters:
                if guy.name == dude.name:
                    out.append(dude)
        return out
    
    def pitchersOnTeam(self,team):
        out = []
        for guy in self.CBSPitchers.listOfGuysOnTeam(team):
            for dude in self.FGPitchers:
                if guy.name == dude.name:
                    out.append(dude)
        return out

    def assignEligibilities(self):
        for guy in self.CBSHitters:
            for dude in self.FGHitters:
                if dude.name == guy.name:
                    for pos in guy.elig:
                        dude.addElig(pos)
                    break
        
    
    def freeAgentPitchers(self):
        out = []
        temp = []##for efficiency, we append guys to this and then remove them during iterations below.
        for guy in self.CBSPitchers.listOfFreeAgents():
            for dude in self.FGPitchers:
                if dude.name == guy.name:
                    out.append(dude)
                    temp.append(dude)
                    self.FGPitchers.remove(dude)##don't iterate over him any more.
                    break##you aren't finding anotherone, so stop
        self.FGPitchers.extend(temp)
        
        return out
        
    def freeAgentHitters(self):
        out = []
        temp = []
        for guy in self.CBSHitters:
            for dude in self.FGHitters:
                if dude.name == guy.name:
                    out.append(dude)
                    temp.append(dude)
                    self.FGHitters.remove(dude)
                    break
        self.FGHitters.extend(temp)
        
        return out

    
#test()