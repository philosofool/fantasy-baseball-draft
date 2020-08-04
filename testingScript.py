# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 06:15:46 2019

@author: lenha
"""

from BaseClasses.BaseFantasyClasses import ClosersFile
from BaseClasses.BaseFantasyClasses import DepthPitcherFile
from BaseClasses.Pitcher import Pitcher
from BaseClasses.Team import Team
from DraftAssistant import DraftAssistant
import os
import datetime
import re

def test1():
    '''Testing closers file'''
    closers = ClosersFile("closers2019.csv")
    closers.test()
    pitchers = DepthPitcherFile("TestFiles/pitchersProj.csv")
    Pitcher.replacementLevel = pitchers.replacementLevel()
    closers.guysAsPitchers(pitchers)
    #print(closers.listNonPitchers())
    for team in closers.teams:
        try:
            guy = team.closer.name
            fWAR = team.closer.fWAR()
        except:
            guy = "none"
            fWAR = 0.0
        print("{:12.12} {:15} {:4.2f}".format(team.team,guy,fWAR))
        for guy in team.handcuffs:
            try:
                #print(guy.isaPitcher())
                dude = guy.name
                fWAR = guy.fWAR()
                print("{:12.12} {:15.15} {:>5.2f} good".format(team.team,dude,fWAR))
                
            except:
                #print(guy)
                #guy = guy
                fWAR = 0.0
                print("{:12.12} {:15.15} {:>5.1f} bad".format(team.team,guy,fWAR))

    for guy in closers.closersWithStrength("strong") + closers.closersWithStrength("medium") + closers.closersWithStrength("weak"):
        print("{:15.15}  {:2} {:5.1f}".format(guy.name, guy.SV, guy.fWAR()))
    
    print("** Battlers **")
    for team in closers.teams:
        if team.strength.lower() == "battle":
            for guy in team.handcuffs:
                try:
                    print("{:8.8}  {:15.15}  {:2} {:5.1f}".format(team.team, guy.name, guy.SV, guy.fWARc()))
                except:
                    pass
    print("** End of test one.")
    
    
def test2():
    '''Testing Team functionality'''

def reTest():
    a = "University"
    reg = "univ"
    b = re.match(reg,a,re.I)
    print(b)
    
def assistantTest():
    assist = DraftAssistant(#"Files/stats-main2017hitters.csv",
                   #"TestFiles/hittersOwned.csv",
                   #"TestFiles/pitchersOwned.csv",
                   #"horseShitHitters.csv",
                   #"horseShitPitchers.csv",
                   "dummyHitters.csv",
                   "dummyPitchers.csv",
                   "Projections/hittersProj_2_27_2019.csv",
                   "Projections/pitcherProj_2_27_2019.csv"
                   )
    
    dlfldr = "/Users/Lenhart/Downloads/2019"
    
    #print(assist.eligHitters.repeatedPlayerNames)
    #print(assist.eligPitchers.repeatedPlayerNames)
    assist.teamName = "Omak Wrong Players"
    assist.setMyTeam()
    assist.myTeam.setLineUp()
    assist.myHandcuffs()
    assist.basicAnalysis()
    print(assist.fileIsPitchers('dummyPitchers.csv'))
    print(assist.fileIsHitters('dummyHitters.csv'))
    assist.update('dummyHitters.csv','dummyPitchers.csv')
    assist.update('','')
    assist.klfTeams()

def fileosTest():
    files = []
    print(os.path.abspath('.'))
    path = "/Users/lenhart/Downloads/2019"
    #path = "."
    with os.scandir(path) as it:
        for e in os.scandir(path):
            files.append(e)
    it.close()
    files.sort(key = lambda file: file.stat().st_ctime)
    #for e in files:
    #    print(e, e.stat().st_ctime)
    dudes = open(files[-1],'r')
    dudes.close()
    print(datetime.datetime.utcfromtimestamp(files[-1].stat().st_ctime))
    print(os.name)
    #print(dudes.readline())
    #print(dudes.readline())
    #x = open(files[-2],'r')
    #print(x.readline())
    #print(type(e))
    #print(isinstance(e,os.DirEntry))
    
def irrelevant():
    print("{}{}".format("1\n1","1\n1"))
        
    

    
#test1()
#assistantTest()
#fileosTest()
reTest()