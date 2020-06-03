# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 07:27:18 2017
Last modified Sat Feb 2 2019


@author: lenhart

This file contains a DraftAssistant class definition for a list of player probjects and player CBS availablities
It can be updated to reflect changed in eligibility
.

"""

from BaseClasses.player.Pitcher import Pitcher
from BaseClasses.player.Hitter import Hitter
from BaseClasses.team.Team import Team
from BaseClasses.BaseFantasyClasses import SimplePlayer
from BaseClasses.BaseFantasyClasses import ClosersFile
from BaseClasses.BaseFantasyClasses import CBSFilePlayers
from BaseClasses.BaseFantasyClasses import HitterFile
from BaseClasses.BaseFantasyClasses import DepthPitcherFile
from BaseClasses.BaseFantasyClasses import CBSHitterProjections
##from BaseClasses.BaseFantasyClasses import PitcherFile

import csv
import os
import re
from datetime import datetime



def test():#for testing.
#    q = DraftAssistant(#"Files/stats-main2017hitters.csv",
#                       "Files/CBSHitters.csv",
#                       "Files/CBSPitchers.csv",
#                       "FGDepthProjections2017.csv",
#                       "FGDepthProjections2017Pitchers.csv"
#                       )
#    cbs = CBSHitterProjections("cbs2019HitterProj.csv")
#    cbs.sort(key = lambda player : player.fWAR600(), reverse = True)
#    n = 1
#    for guy in cbs[0:200]:
#        print("{:3} {:20} {:.4f}".format(n, guy.name, guy.fWAR600()))
#        n += 1
    hitProj = "Projections/FGDepth_Feb22.csv"#yes, the names of the files are backwards
    pitProj = "Projections/FGDepthPitchers_Feb22.csv"
    a = "TrueTalent(26).csv"
    b = "TrueTalent(27).csv"
    cbsHit = "hittersDrafting.csv"
    cbsPit = "pitchersDrafting.csv"
    q = DraftAssistant(
                       # a,
                       # b,
                       cbsHit,
                       cbsPit,
                       hitProj,
                       pitProj
                       )
    q.teamName = "Omak"
    q.setMyTeam()
    q.sortByfWAR()
    q.myTeam.setLineUp()
    x = q.setCatcherReplacement()
    for guy in q.myTeam.players:
        if guy.name == "Eloy Jimenez":
            guy.adjToPA(630)
        elif guy.name == "Francisco Lindor":
            guy.adjToPA(500)
    #print(q.notFound)
    
    q.hitters = q.freeAgentHitters()
    q.pitchers = q.freeAgentPitchers()    
    q.sortByfWAR()
    #q.printHitters()
    #q.printPitchers()
#    for guy in q.hitters[180:190
#                         ]:
#        print(q.assistLineHitter(guy))
    q.printCheatSheetFile("cheatSheet.txt")
    #print("Integrating some new CBS stuff...")
    #q.integrateCBS("stats.csv","stats (1).csv")
    q.setMyTeam()
    q.myTeam.setLineUp()
    q.basicAnalysis(q.myTeam)
    q.update("","")
    #print(q.closerReport())
    #print(q.stealsReport())
    #print(q.closerBattleReport())

    teams = q.constructklfTeams()
    teams.remove(None)
    q.klfTeams.pop(None)
    q.findklfTeam("bus")
    #print(q.bestRelievers())
    #print(q.myTeam.targetStats())
    #for guy in q._allPitchers[1:10]:
    #    if not guy.isReliever():
    #        print(guy.spgLine())
    while q.getInput():
        pass
    
    with open("leagueSummary.txt",'w') as summary:
        for team in teams:
            summary.write(team+"\n")
            it = q.klfTeams[team]
            #q.basicAnalysis(it)
            summary.write(it.printLineUp())
            summary.write(it.teamTotals()+"\n")
    summary.close()
    
def seasonAssist():
    cbsHit = "cbsHitters_3_21.csv"
    cbsPit = "cbsPitchers_3_21.csv"
    
    
def removeSomeGuys(team):
    '''This is just a little hack to get rid of players that are in my roster'''
#    guys = [Hitter Vladimir Guerrero Jr., Hitter Tyler O'Neill, Hitter Starlin Castro, Hitter Shohei Ohtani, Hitter Shin-Soo Choo, Hitter Robinson Chirinos, Hitter Matt Chapman, Hitter Francisco Lindor, Hitter Eloy Jimenez, Hitter Denard Span, Hitter Danny Jansen, Hitter Daniel Murphy, Hitter Brandon Belt, Pitcher Steve Cishek, Pitcher Rick Porcello, Pitcher Richard Rodriguez, Pitcher Jose Quintana, Pitcher Jordan Zimmermann, Pitcher Jameson Taillon, Pitcher David Robertson, Pitcher Brad Peacock]
    a = [
            #"Vladimir Guerrero Jr.",
            "Tyler O'Neill",
            "Starlin Castro",
            "Shohei Ohtani",
            "Shin-Soo Choo",
            "Robinson Chirinos",
            "Matt Chapman",
            #"Francisco Lindor",
            #"Eloy Jimenez",
            "Denard Span",
            "Danny Jansen",
            #"Daniel Murphy",
            "Brandon Belt",
            "Steve Cishek",
            "Rick Porcello",
            "Richard Rodriguez",
            "Jose Quintana",
            "Jordan Zimmermann",
            "Jameson Taillon",
            "David Robertson",
            "Brad Peacock"
            ]
    temp = []
    for guy in team.players:
        #print(guy.name)
        if guy.name in a:
            #print("     removing {}".format(guy.name))
            temp.append(guy)
    for guy in temp:
        team.removePlayer(guy)
    
#class SeasonAssistant(DraftAssistant):
#    '''
#    I don't know if this is going to work. The main difference between this and a draft assistant is probably just 
#    the source files. 
#    '''

class Assistant:
    def __init__(self,hitterFile,pitcherFile):
        
                
        ##eligHitters is a .csv file from CBS that contains a list of all hitters; 
        ##it should be only those players who are eligible to be drafted.
        ##hitterProjections is a .csv from Fangraphs that contains a list of projections.
        ##eligPitchers and pitcherProjections are similar files for pitchers.
                
        self.hitters = HitterFile(hitterProjections)
        self.pitchers = DepthPitcherFile(pitcherProjections)
        Hitter.replacementLevel = self.hitters.replacementLevel()
        Pitcher.replacementLevel = self.pitchers.replacementLevel()
        self._allHitters = self.hitters
        self._allPitchers = self.pitchers

        self.integrateCBS(eligHitters,eligPitchers,False)
        
        self.closerFile = ClosersFile("closers2019.csv")
        self.closerFile.guysAsPitchers(self._allPitchers)
                
        self.myTeam = Team([])
        self.teamName = None
        if os.name == 'posix':#on a mac
            self.downloadsFolder = "/Users/lenhart/Downloads/2019"##on your mac
        elif os.path.exists("/Users/sjl98/Downloads/2019"):##office computer
            self.downloadsFolder = "/Users/sjl98/Downloads/2019"
        elif os.path.exists("/Users/Lenhart/Downloads/2020"):##home computer
            self.downloadsFolder = "/Users/Lenhart/Downloads/2020"##Not typical for an __init__ to be so specific, this is helpful for my future.
        else:
            raise FileNotFoundError("Could not find directory for downloads on this computer.")
        with open('remember.txt','r') as remember:
            self.remember = remember.read()
        remember.close()

    def sortByfWAR(self):
        self.hitters.sort(key=lambda hitter : hitter.fWAR(), reverse= True)
        self.pitchers.sort(key=lambda pitcher : pitcher.fWAR(), reverse= True)
        self._allHitters.sort(key=lambda hitter : hitter.fWAR(), reverse= True)
        self._allPitchers.sort(key=lambda pitcher : pitcher.fWAR(), reverse= True)
        
    def sortByRatefWAR(self):
        self.hitters.sort(key=lambda hitter : hitter.fWAR600(), reverse= True)
        self.pitchers.sort(key=lambda pitcher : pitcher.fWAR150(), reverse= True)
        
    def setCatcherReplacement(self):
        catchers = self.guysEligAt("C")
        Hitter.catcherReplacement = catchers[15].rawWAR()
        return catchers[15].rawWAR()
    
    @staticmethod
    def assistLineHitter(guy):
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        basic = '{0:20} {1:10} {2:11} {3:6.2f} {4:5.2f} '.format(guy.name[0:17],team, guy.printElig(), guy.fWAR(), guy.fWAR600())
        full = '   PA {5:3.0f}  BA {0:.3f}  RBI {1:3.0f}  R {2:3.0f}  HR {3:2.0f}  SB {4:2.0f}   ADP {6:6}'.format(guy.BA(), guy.RBI, guy.R, guy.HR, guy.SB, guy.PA, guy.ADP)
        return (basic + full)
        
    @staticmethod
    def assistLinePitcher(guy):
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        
        basic = '{0:20} {1:10} {4:11} {2:6.2f} {3:5.2f} '.format(guy.name[0:17],team, guy.fWAR(), guy.fWAR150(), guy.printElig())
        full = '   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:3.0f}  W {4:2.0f}  SV {5:2.0f}  ADP {6:6}'.format(guy.IP, guy.ERA(), guy.WHIP(), guy.SO,  guy.W, guy.SV, guy.ADP)
        return (basic + full)




class DraftAssistant(Assistant):
    
    positions = ["C","1B","2B","3B","SS","RF","CF","LF","U","IF","OF"]
    
    def __init__(self,eligHitters,eligPitchers,hitterProjections,pitcherProjections):
        
                
        ##eligHitters is a .csv file from CBS that contains a list of all hitters; 
        ##it should be only those players who are eligible to be drafted.
        ##hitterProjections is a .csv from Fangraphs that contains a list of projections.
        ##eligPitchers and pitcherProjections are similar files for pitchers.
                
        self.hitters = HitterFile(hitterProjections)
        self.pitchers = DepthPitcherFile(pitcherProjections)
        Hitter.replacementLevel = self.hitters.replacementLevel()
        Pitcher.replacementLevel = self.pitchers.replacementLevel()
        self._allHitters = self.hitters
        self._allPitchers = self.pitchers

        self.integrateCBS(eligHitters,eligPitchers,False)
        
        self.closerFile = ClosersFile("closers2019.csv")
        self.closerFile.guysAsPitchers(self._allPitchers)
                
        self.myTeam = Team([])
        self.teamName = None
        if os.name == 'posix':#on a mac
            self.downloadsFolder = "/Users/lenhart/Downloads/2019"##on your mac
        elif os.path.exists("/Users/sjl98/Downloads/2019"):##office computer
            self.downloadsFolder = "/Users/sjl98/Downloads/2019"
        elif os.path.exists("/Users/Lenhart/Downloads/2019"):##home computer
            self.downloadsFolder = "/Users/Lenhart/Downloads/2019"##Not typical for an __init__ to be so specific, this is helpful for my future.
        else:
            raise FileNotFoundError("Could not find directory for downloads on this computer.")
        with open('remember.txt','r') as remember:
            self.remember = remember.read()
        remember.close()
        
        
    def integrateCBS(self,hitters,pitchers,update=True):
        '''Integrate data from CBS into player projections based on new CBS files
        This can be used to update at any time.... if it works right.'''
        try:
            self.eligHitters = CBSFilePlayers(hitters)
            self.eligPitchers = CBSFilePlayers(pitchers)
        except:
            print("Could not update from CBS files {} (hitters) and {} (pitchers)".format(hitters,pitchers))
        self.eligHitters.sortByName()
        self.eligPitchers.sortByName()
        
        if not update:
            self.checkNames()
            for guy in self.notFound:
                self.fixName(guy)
            self.checkNames()
            self.setHitterElig()
            self.setCatcherReplacement()
            self.constructklfTeams()
            print("The following players were not found in CBS data.")
            print(self.notFound)
        self.sortByfWAR()
        self.setAvail()
        if update:
            try:
                self.setMyTeam()
            except:
                print("setMyTeam failed in integrateCBS.")
                
            try:
                self.myTeam.setLineUp()
            except:
                self.myTeam.setLineUp()
                print("myTeam.SetLineUp() failed in integrateCBS.")
                
    def checkNames(self):
        '''
        Does a few things:
            -checks for names that are repeated.
            -checks for guys in projections but not found in CBS; usually a difference in name (Dan/Daniel)
        '''
        temp = self._allHitters + self._allPitchers
        if not self.eligHitters.repeatedPlayerNames:
            self.eligHitters.repeatedNames()
        if not self.eligPitchers.repeatedPlayerNames:
            self.eligPitchers.repeatedNames()
        self.repeatedNames = self.eligHitters.repeatedPlayerNames + self.eligPitchers.repeatedPlayerNames
        temp = set()
        notFound = []
        for guy in self._allHitters:
            for dude in self.eligHitters:
                if guy.name == dude.name:
                    temp.add(guy)
                    break
            if guy not in temp:
                #guy.avail = None
                notFound.append(guy)
                
        temp = set()
        for guy in self._allPitchers:
            for dude in self.eligPitchers:
                if guy.name == dude.name:
                    temp.add(guy)
                    break
            if guy not in temp:
                notFound.append(guy)
        self.notFound = notFound
        #self.removeUnfound()

    def removeUnfound(self):
        for guy in self.notFound:
            if guy in self._allHitters:
                self._allHitters.remove(guy)
                print("{} was removed from self._allHitters".format(guy,self))
            elif guy in self._allPitchers:
                self._allPitchers.remove(guy)
                print("{} was removed from self._allPitchers".format(guy))
            else:
                print("{} in {} was not in allPlayer data.".format(guy,self.notFound,self._allHitters,self._allPitchers))
                
        
            
        
    def setMyTeam(self):
        '''puts guys on self.teamName on a self.myTeam'''
        teamName = self.teamName.lower()
        #print(teamName)
        #hitters = CBSFilePlayers.playerIntersection(self.hitters,self.eligHitters.listOfGuysOnTeam(teamName))
        #pitchers = CBSFilePlayers.playerIntersection(self.pitchers,self.eligPitchers.listOfGuysOnTeam(teamName))
        self.myTeam.reset()
        for guy in self._allHitters + self._allPitchers:
            if guy.avail == None:
                pass##fuck off an die, Michael Lorenzen
            elif guy.avail.lower()[:4] == teamName[:4]:
                self.myTeam.addAPlayer(guy)
        #self.myTeam.addPlayers(myTeam)
        
    def constructklfTeams(self):
        teams = []
        for guy in self._allPitchers + self._allHitters:
            if not guy.isFreeAgent() and guy.avail not in teams:
                teams.append(guy.avail)
            #if len(teams) >= 16:
             #   break
        #teams.remove(None)
        self.klfTeams = {}
        for team in teams:
            self.klfTeams[team] = Team([])
            self.klfTeams[team].name = team
        for guy in self._allHitters + self._allPitchers:
            if not guy.isFreeAgent():
                self.klfTeams[guy.avail].addAPlayer(guy)
        for team in self.klfTeams:
            self.klfTeams[team].setLineUp()
        
            
        return teams
    
    def findklfTeam(self,teamname):
        for team in self.klfTeams:
            #print(team)
            x = re.match(teamname,team,re.I)
            if x != None:
                print("sending you the {}".format(team))
                out = self.klfTeams[team]
                return out
            else:
                pass
        return None

    
    def _test(self):
        '''this is for checking if the thing is creating errors'''                                      
        check = 1
        print("Verifying {}".format(self))
        print("Repeated names in hitters: ".format(self.eligHitters.repeatedNames()))
        print("Repeated names in pitchers: ".format(self.eligPitchers.repeatedNames()))

        print("Check {}...".format(check),self)
        self.sortByRatefWAR()
        positions = ["1B","2B","3B","SS","RF","CF","LF","C"]
        print("Check {}...",len(self.eligAt(positions)))
        self.sortByfWAR()
        self.printHitters(12)
        print()
        self.printPitchers(12)
        self.pitchers = []
        for guy in self.pitchers:
            if guy.hasSaves(4):
                self.pitchers.append(guy)
        self.pitchers.sort(key=lambda guy: guy.team)
        print(len(self.pitchers))
        self.printPitchers(100)
        print(type(self.hitters))
            
    #    print()
    #    for position in positions:
    #        print("{} eligible hitters:\n".format(position))
    #        temp = [position]
    #        q.printHittersbyPosAndfWAR(position,0)
    #        print("\n\n")
        
        print("Finished with test().\n")
        return None


    
    def setHitterElig(self):
        #tempset = set()##what is this for?
        for player in self.hitters:
            for guy in self.eligHitters:
#                if "-" in guy.name:
#                    tempset.add(guy.name)
                if guy.name == player.name:
                    if guy.name in self.eligHitters.repeatedPlayerNames:
                        pass##this is fucking why lorenzen etc. don't work...
                    else:
                        for key in guy.elig:
                            if key == "U":
                                pass
                            else:                            
                                player.elig[key] = True
        
        
    def guysEligAt(self,position):
        '''
        Returns a list of guys eligible at a position in positions. Positions
        is a list of strings, "CF", "C" etc.
        if positions == [], it returns all the players.
        '''
        out = []
#        if positions == []:
#            return self.hitters
#        for hitter in self.hitters:
#            for i, v in hitter.elig.items():
#                if v == True:
#                    if i in positions:
#                        out.append(hitter)
#                        break
#        return out
        for guy in self.hitters:
            if guy.elig[position]:
                if guy not in out:
                    out.append(guy)
        return out
    
    def pickValues(self):
        temp = self._allHitters + self._allPitchers
        temp.sort(key= lambda guy: guy.fWAR(), reverse = True)
        picks = (24 * 15)
        out = "{:2} {:3} {:3}\n".format("Rnd","Pick","Value")
        for i in range(picks):
            draftRnd = int(i/15) + 1
            out += "{:3} {:4} {:5.2f}\n".format(draftRnd,i,temp[i].fWAR())
        return out
    
    def printHitters(self, n = 8):
        for hitter in self.hitters[:n]:
            print(self.assistLineHitter(hitter))
            
    def printPitchers(self,n = 8):
        for pitcher in self.pitchers[0:n]:
            print(self.assistLinePitcher(pitcher))

    def printPitchersByfWAR(self,n=8):
        temp = self.pitchers
        temp.sort(key=lambda guy: guy.fWAR(), reverse = True)
        for guy in temp[0:n]:
            print(self.assistLinePitcher(guy))
            
    def printRelieversByfWAR(self,n=20):
        temp = []
        for guy in self.pitchers:
            if guy.isReliever():
                temp.append(guy)
        temp.sort(key=lambda guy: guy.fWAR(), reverse = True)
        for guy in temp[0:n]:
            print(self.assistLinePitcher(guy))
        
            
    def printHittersbyPosAndfWAR(self,positions,fWAR):
        '''print all guys eligible at positions with minimum fWAR'''
        temp = self.eligAt(positions)
        ##print("Temp 0 is ", temp[0])
        temp.sort(key=lambda guy: guy.fWAR(), reverse = True)
        for guy in temp:
            if guy.fWAR() >= fWAR:
                print(self.assistLineHitter(guy))
            else:
                break
            
    def setAvail(self):
        '''sets each player's freeagent/owner status'''
        temp = set()
        notFound = []
        ##you could speed this up by making a temp list of self.hitters and sorting by name, but it doesn't seem too slow.
        for guy in self._allHitters:
            for dude in self.eligHitters:
                if guy.name == dude.name:
                    guy.avail = dude.avail
                    temp.add(guy)
                    break
            if guy not in temp:
                guy.avail = None
                notFound.append(guy)
                
            
        for guy in self._allPitchers:
            for dude in self.eligPitchers:
                if guy.name == dude.name:
                    guy.avail = dude.avail
                    temp.add(guy)
                    break
            if guy not in temp:
                guy.avail = None
                notFound.append(guy)
        return notFound                

    def playersOnTeam(self,team):
        '''get a list of the players on team with name team'''
#        temp = []
#        for guy in self.eligHitters:
#            if guy.avail[0:3].lower() == team[0:3].lower():
#                #print(guy.name)
#                temp.append(guy)
#        self.hitters = CBSFilePlayers.playerIntersection(self.hitters,temp)        
#        temp2 = []
#        for guy in self.eligPitchers:
#            if guy.avail[0:3].lower() == team[0:3].lower():
#                #print(guy.name)
#                temp2.append(guy)
#        self.pitchers = CBSFilePlayers.playerIntersection(self.pitchers,temp2)
#        return self.pitchers + self.hitters
        team = team.name.lower()[:4]
        out = []
        for guy in self._allHitters:
            if str(guy.avail).lower()[:4] == team:
                out.append(guy)
        for guy in self._allPitchers:
            if str(guy.avail).lower()[:4] == team:
                out.append(guy)
        return out
                
    
    def freeAgentPitchers(self):
        out = []
        for guy in self._allPitchers:
            if guy.isFreeAgent():
                out.append(guy)
        return out
    
    def freeAgentHitters(self):
        out = []
        for guy in self._allHitters:
            try:
                if guy.isFreeAgent():
                    out.append(guy)               
            except TypeError:
                print(guy.name)
        return out
    
    def closerReport(self, complete = True):
        teams = self.closerFile.teams
        outstring = "{:10.10} {:6.6}  {:1}{}\n"
        out = ""
        strengths = ["strong","medium","weak"]
        for strength in strengths:
            teams = self.closerFile.teamsWithStrength(strength)
            teams.sort(key = lambda team : team.closer.fWAR(), reverse = True)
            for team in teams:
                if team.closer.isFreeAgent():
                    x = ""
                else:
                    x = "*"
                out += outstring.format(team.name, team.strength, x,self.assistLinePitcher(team.closer))
                
        return out

    def closerBattleReport(self):
        teams = self.closerFile.teams
        outstring = "{:10.10} {:6.6}  {:1}{}\n"
        out = ""
        print("Fucking hell, you're looking at guys in position battles...")
        for team in self.closerFile.teamsWithStrength("battle"):
            for guy in team.handcuffs:
                if guy.isFreeAgent():
                    x = ""
                else:
                    x = "*"
                try:
                    if float(guy.ADP) < 500:
                        out += outstring.format(team.name, team.strength, x,self.assistLinePitcher(guy))
                except:
                    pass
        return out
    
    def myHandcuffs(self):
        '''List handcuffs for my closers.'''
        teams = []
        out = ""
        for guy in self.myTeam:
            if guy.isReliever():
                if guy.team not in teams:
                    teams.append(guy.team)
        for team in self.closerFile.teams:
            if team.name in teams:
                for guy in team.handcuffs:
                    try:
                        out += self.assistLinePitcher(guy) + "\n"
                    except:
                        pass
        return out
    
    def bestRelievers(self, n = 7):
        out = ""
        i = 0
        for guy in self._allPitchers:
            if guy.isFreeAgent() and guy.isReliever():
                out += self.assistLinePitcher(guy)+"\n"
                if i > n:
                    break
                i += 1
        return out
    
    def stealsReport(self):
        guys = self.freeAgentHitters()
        guys.sort(key = lambda guy:guy.SB, reverse = True)
        out = ""
        if len(guys) < 8:
            n = len(guys)
        else:
            n = 8
        for guy in guys[:n]:
            out += self.assistLineHitter(guy) + "\n"
        return out
    
    def freeAgentsAtPos(self,positions):
        '''free agents at positions.
        --pos is a list of postion abbreviations (e.g, "CF") separated by spaces and may include commas.
        '''

        guys = self.freeAgentHitters()
        out = []
        for pos in positions:
            if pos not in self.positions:##ignore bad strings
                pass
            else:
                for guy in guys:
                    if guy.elig[pos]:
                        if guy not in out:
                            out.append(guy)
                    elif pos == "IF" and (guy.elig("CI") or guy.elig("MI")):
                        if guy not in out:
                            out.append(guy)
        return out
    
    def listFreeAgentsAt(self,positions):
        '''
        for command line input...
        lists the free agents. 
        This mostly just turns a string input into a list and passes to 
        self.freeAgentsAtPos()
        '''
        x = positions.strip()
        x = x.split(" ")
        positions = []
        for e in x:
            positions.append(e.strip().upper())
        guys = self.freeAgentsAtPos(positions)
        guys.sort(key = lambda dude: dude.fWAR(), reverse= True)
        out = ''
        for guy in guys[:9]:
            out += guy.assistLine() + "\n"
        return out


    def printPlayersOnTeam(self,team,byRate=False,n=20):
        self.playersOnTeam(team)
        if not byRate:
            self.sortByfWAR()
        else:
            self.sortByRatefWAR()
        m = 0
        o = 0
        for guy in self.hitters:
            print(self.assistLineHitter(guy))
            m = m + 1
            if m > n:
                break
        for guy in self.pitchers:
            o = o + 1
            if o > n:
                break
            print(self.assistLinePitcher(guy))

    def teamsSummary(self):
        '''This is a half assed summary of teams'''
        players = self._allHitters + self._allPitchers
        for player in players:
            if player.avail == None:
                print(player)
                players.remove(player)
        players.sort(key = lambda guy: guy.avail)
        for guy in players:
            try:
                if not guy.isFreeAgent():
                    print("{:18} {:16} {:3.1f}".format(guy.avail[:15],guy.name[:15],guy.fWAR()))
            except:
                print(guy,guy.name)
                
    def printCheatSheetFile(self,filename):
        file = open(filename,"w")
        file.write("Fantasy Baseball 2019 Projections\n")
        file.write("SP\n")
        rank = 1
        for guy in self._allPitchers:
            if guy.GS > 5:
                if guy.isFreeAgent():
                    fa = ""
                else:
                    fa = "*"
                file.write("{:3} {}{:20} {:3.1f}\n".format(rank,fa,guy.name,guy.fWAR()))
                rank += 1
                if rank > 120:
                    break
        file.write("\nRP\n")
        rank = 1
        for guy in self._allPitchers:
            if guy.GS < 5:
                if guy.isFreeAgent():
                    fa = ""
                else:
                    fa = "*"
                file.write("{:3} {}{:20} {:3.1f}\n".format(rank,fa,guy.name,guy.fWAR()))
                rank += 1
                if guy.fWAR() < 0:
                    break
        pos = self.hitters[0].elig.keys()
        #print(pos)
        for i in pos:
            rank = 1
            file.write("\n"+i+"\n")
            for guy in self._allHitters:
                if guy.elig[i]:
                    if guy.fWAR() < 0:
                        break
                    else:
                        if guy.isFreeAgent():
                            fa = ""
                        else:
                            fa = "*"
                        file.write("{:3} {}{:20} {:>3.1f}\n".format(rank,fa,guy.name,guy.fWAR()))
                        rank += 1
        everyone = self._allHitters + self._allPitchers
        everyone.sort(key = lambda guy:guy.fWAR(), reverse = True)
        rank = 1
        file.write("\nEveryone")
        for guy in everyone:
            if guy.isFreeAgent():
                fa = ""
            else:
                fa = "*"
            file.write("{:3} {}{:20} {:3.1f}\n".format(rank,fa,guy.name,guy.fWAR()))
            rank += 1
            if guy.fWAR() < 0:
                break

        file.close()
        
    def basicAnalysis(self,team):
        print(team.printLineUp())
        print(team.teamTotals())
        print(team.teamAnalysis())
        print(team.teamSPGAnalysis())

    def update(self,hitters,pitchers):
            '''
            This is going to be somewhat complicated. But awesome.
            First, try updating with the most recent files in you downloads folder.
            Second, try updating from the downloads folder by the specified names.
            '''
            if hitters == "" and pitchers == "":##look for the most recent correct files in self.downloads
                ##use the most recent in the dlfldr
                path = self.downloadsFolder
                files = []
                with os.scandir(path) as it:
                    for e in os.scandir(path):
                        files.append(e)
                it.close()
                files.sort(key = lambda file: file.stat().st_ctime, reverse = True)
                for file in files:
                    if self.fileIsHitters(file):
                        hitters = file
                        cdate = datetime.fromtimestamp(file.stat().st_ctime)
                        print("Newest hitters file is {}, {}".format(hitters.name, cdate))
                        break
                for file in files:
                    if self.fileIsPitchers(file):
                        pitchers = file
                        cdate = datetime.fromtimestamp(file.stat().st_ctime)
                        print("Newest pitchers file is {}, {}".format(pitchers.name, cdate))
                        break
                try:
                    self.integrateCBS(hitters,pitchers)
                    print("Updated with latest hitters and pitchers files.")
                except:
                    print("Could not update latest hitters and pitchers.")

            else:##make the name a .csv if it isn't
                if hitters[-4:] != '.csv':
                    hitters += '.csv'
                if pitchers[-4:] != '.csv':
                    pitchers += '.csv'
                if hitters in os.listdir(self.downloadsFolder):
                    hitters = self.downloadsFolder + hitters
                else:
                    print("{} (hitters) not in {}".format(hitters,self.downloadsFolder))
                if pitchers in os.listdir(self.downloadsFolder):
                    pitchers = self.downloadsFolder + pitchers
                else:
                    print("{} (pitchers) not in {}".format(pitchers,self.downloadsFolder))
                try:
                    if self.fileIsHitters(hitters) and self.fileIsPitchers(pitchers):
                        self.integrateCBS(hitters,pitchers)
                    elif self.fileIsPitchers(hitters) and self.fileIsHitters(pitchers):
                        print("I think you got the names backwards.")
                        self.integrateCBS(pitchers,hitters)
                    print("Update complete.")
                except FileNotFoundError:
                    print("File not found. typo in '{}' or '{}'?".format(pitchers,hitters))
                    
    def fileIsHitters(self,filename):
        if isinstance(filename,os.DirEntry):
            if filename.name[-4:] != ".csv":
                return False
        elif filename[-4:] != ".csv":
            return False
        with open(filename) as it:
            it.readline()
            a = it.readline()
        it.close()
        #print(a)
        if 'AB' in a:
            return True
        else:
            return False
    
        
    def fileIsPitchers(self,filename):
        if isinstance(filename,os.DirEntry):
            if filename.name[-4:] != ".csv":
                return False
        elif filename[-4:] != ".csv":
            return False
        with open(filename) as it:
            it.readline()
            a = it.readline()
        it.close()
        #print(a)
        if 'INN' in a or 'IP' in a:
            return True
        else:
            return False
            
        
    def getInput(self):
        #self.basicAnalysis()
        helpString = """
        'update': loads fresh CBS data from two files.
        'pos' will list hitters/pitchers at positions.
        'best' will list top 6 hitters and pitchers.
        'closers' will list relief pitchers.
        'battles' will list closer position battles.
        'handcuffs' will list those for my closers.
        'steals' to see who has steals.
        'name' will give your team a new name.
        'lookup' to look guys up. 
        'best rate' to list guys by rate stats.
        'remember' will give you some reminders.
        'competition' will let you look at other teams.
        'relief' lists best relievers.
        """
        x = input("What do you need? 'help' for info. ").strip().lower()
        if x == 'help':
            print(helpString)
        elif x == 'update':
            pitchers = input("Pitcher file name? ").strip()
            hitters = input("Hitter file name? ").strip()
            self.update(hitters,pitchers)
            #except:
             #   print("There was some damned error updating your file...")
        elif x == 'best':
            for guy in self.freeAgentHitters()[:6]:
                print(guy.assistLine())
            for guy in self.freeAgentPitchers()[:6]:
                print(guy.assistLine())
            
        elif x == 'needs':
            pass
        elif x == 'remember':
            print(self.remember)
        elif x == 'pos':
            pos = input("What positions would you like to view?").strip()
            print(self.listFreeAgentsAt(pos))
            if 'p' in pos.lower().split(' '):
                for guy in self.freeAgentPitchers()[:5]:
                    print(self.assistLinePitcher(guy))
                
        elif x == 'best rate':
            hitters = self.freeAgentHitters()
            pitchers = self.freeAgentPitchers()
            hitters.sort(key=lambda guy:guy.fWAR600(), reverse = True)
            pitchers.sort(key=lambda guy:guy.fWAR150(),reverse = True)
            n = 0
            
            for guy in hitters:
                if guy.PA > 30:
                    print(guy.assistLine())
                    n += 1
                    if n >= 8:
                        break
            n = 0
            for guy in pitchers:
                if guy.IP > 10:
                    print(guy.assistLine())
                    n += 1
                    if n >= 5:
                        break
        elif x == 'myteam':
            self.basicAnalysis(self.myTeam)
        elif x[:4] == 'competition'[:4]:
            team = input("What KLF team do you want to view?").strip()
            team = self.findklfTeam(team)
            try:
                team.setLineUp()
                print(team.name)
                print(self.basicAnalysis(team))
            except:
                pass
        elif x == 'name':
            name = input("What's your new team name? ")
            self.teamName = name
            self.setMyTeam()
            self.myTeam.setLineUp()
        elif x == 'lookup':
            guy = input("Who do you want to look up? ").lower().strip()
            for dude in self._allHitters:
                if guy in dude.name.lower():
                    print("{:5.5} {}".format(str(dude.avail),dude.assistLine()))
                    #guy = dude.asNumberPA(600)
                    print("{:5.5} {}".format(str(""),dude.asNumberPA(600).assistLine()))
            for dude in self._allPitchers:
                if guy in dude.name.lower():
                    print("{:5.5} {}".format(dude.avail,dude.assistLine()))
                    print("{:5.5} {}".format(str(""),dude.asNumberIP(150).assistLine()))
        elif x == 'closers':
            print(self.closerReport())
        elif x == 'battles':
            print(self.closerBattleReport())
        elif x == 'handcuffs':
            print(self.myHandcuffs())
        elif x == 'steals':
            print(self.stealsReport())
        elif x == 'exit':
            return False
        elif x == 'relief':
            print(self.bestRelievers())
        return True##you can run in a while loop....
        
            
        
        
    
    def fixName(self,guy):
        '''this is for handling names that don't fit the CBS formating.
        Issues include hyphens, Dan/Daniel, ends with 'Jr.' etc.
        '''
        names = {##this is a concordance of fangraphs names and cbs names. The key is a fangraphs name, which will be the hitter/pitcher name, the value it the CBS name.
                "Michael A. Taylor": "Michael Taylor",
                "Nathaniel Lowe": 'Nate Lowe',
                #"Michael Lorenzen": "Michael Lorenzen",##he's a two way player. it's breaking things.
                'Javier Guerra':'Javy Guerra',
                'J.T. Riddle': 'JT Riddle',
                'Dan Vogelbach':'Daniel Vogelbach',
                'D.J. Stewart': 'DJ Stewart',
                'Cedric Mullins II': 'Cedric Mullins',
                'A.J. Reed': 'AJ Reed',
                'Nathan Karns': 'Nate Karns',
                'Michael Soroka': 'Mike Soroka',
                'Matt Davidson':"Matt Davidson",##two way player, very annoying
                'Joshua James': 'Josh James',
                'Jean Carlos Mejia': 'Jean-Carlos Mejia',
                'Jakob Junis': 'Jake Junis',
                'Daniel Poncedeleon': 'Daniel Ponce de Leon',
                'Zach Britton':'Zack Britton',
                'Luis Alexander Basabe':'Luis Alejandro Basabe',
                'Peter Alonso':'Pete Alonso',
                'Giovanny Urshela':'Gio Urshela',
                'Nicholas Castellanos':'Nick Castellanos',
                'Michael Brosseau':'Mike Brosseau',
                'Abraham Toro' : 'Abraham Toro-Hernandez',
                ##Hitter Michael Lorenzen,
                'Yu-Cheng Chang' : 'Yu Chang',
                'Deivy Grullon':'Deivi Grullon',
                'Steve Wilkerson' : 'Stevie Wilkerson',
                'Kwang-hyun Kim':'Kwang Hyun Kim',
                'JT Brubaker' : 'J.T. Brubaker',
                'Joseph Palumbo' : 'Joe Palumbo',
                ##'Blake Wood' : '',
                'Michael Shawaryn' :'Mike Shawaryn',
                'Josh D. Smith' : 'Josh Smith',
                'Philip Pfeifer': 'Phil Pfeifer',
                #Pitcher Jake Cronenworth,
                #Pitcher 'AJ Ramos':'A.J. Ramos',
                #Pitcher James Shields
                }
        guy.originalName = guy.name
        if guy.name[-4:] == " Jr.":
            guy.name = guy.name.rstrip(" Jr.")
        if guy.name in names.keys():
            guy.name = names[guy.name]
        

 

       
if __name__ == "__main__":
    test()
    #seasonAssist()
