# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 19:57:08 2017

@author: lenhart
"""

from PlayerExtractor import PlayerExtractor
from BaseClasses.BaseFantasyClasses import Team
#from BaseClasses.BaseFantasyClasses import Hitter

def test():
    players = PlayerExtractor("Files/FGDepthProjHitters2017-3-20.csv","Files/FGDepthProjPitchers2017-3-20.csv","Files/CBSHitters.csv","Files/CBSPitchers.csv")
    omak = Team()
    KLFTeam = "SF Bat..."
    omakHitters = players.hittersOnTeam(KLFTeam)
#    for hitter in omakHitters:
#        if hitter.name[0:4] == "J.T.":
#            hitter.addElig("C")
    print(players.teamsInCBS())
    #print(omakHitters)
    #omak.addPlayers(omakHitters)
    omakPitchers = players.pitchersOnTeam(KLFTeam)
    omak.addPlayers(omakHitters)
    omak.addPlayers(omakPitchers)
    omak.sort(key=lambda guy:guy.fWAR(),reverse = False)
    omak.sort(key=lambda guy:guy.isaPitcher(),reverse = False)
#    for i in range(8):
#        omak.pitchers.append(omak.pop())
    omak.sort(key=lambda guy:guy.fWAR(),reverse = False)
    omak.sort(key=lambda guy:guy.isaHitter(),reverse = False)
#    for i in range(10):
#        omak.hitters.append(omak.pop())
#    omak.bench.extend(omak)
#    omak.clear()
#    omak.addPlayers(omak.pitchers+omak.hitters)
    print(omak.TeamTotals())
    ##print(omak.TeamSPGAnalysis())
    print(omak.TeamAnalysis())
        
    
    for guy in omak:
        print("{0:20} {1:2.2f}".format(guy.name, guy.fWAR()))
    
def main():
    pass


#main()
test()    
