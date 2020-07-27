# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:21:30 2019

@author: lenha
"""


class Player:
    '''This is basically just a superclass for hitter and pitcher classes. It handles a lot of shared  stuff between them.
    At some point, I might make it more powerful.
    '''
    def __init__(self):
        '''not much for now, because we mainly create subclass instances.'''
        pass
    
    def isFreeAgent(self):
        '''for fantasy purposes, checks self.avail'''
        try:
            if self.avail == True:
                return True
            elif self.avail[:2] == "FA" or self.avail[:3] == "W (" or self.avail.strip() == "W":
                return True
            else:
                return False
        except:
            return ""
            
    def isOnWaivers(self):
        try:
            if self.isFreeAgent() and "W" in self.avail:
                return True
            else:
                return False
        except AttributeError:
            '''probably no avail yet.'''
            pass
    
#    def isFreeAgent(self):
#    '''This is the version from the Pitcher class definition, which was slightly different from the hitter one. Not sure which should be used.'''
#        '''for fantasy purposes, checks self.avail'''
#        if self.avail == None:
#            print(self, "has no elig; setting to True")
#            return True
#        if self.avail == True:
#            return True
#        elif self.avail[:2] == "FA" or self.avail[:3] == "W (" or self.avail.strip() == "W":
#            return True
#        else:
#            return False

    def printElig(guy):##I don't really like just tacking this on to the file, but....
        out = []
        for i in guy.elig:
            if guy.elig[i]:
                if i not in ["CI","MI","U"]:
                    out.append(i)
        return ",".join(out)
    
    def assistLine(self):
        guy = self
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        
        basic = '{0:20} {1:10} {4:11} {2:6.2f} {3:5.2f} '.format(guy.name[0:17],team, guy.fWAR(), guy.fWAR150(), guy.printElig())
        full = "basic player has no stats"#'   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:3.0f}  W {4:2.0f}  SV {5:2.0f}  ADP {6:6}'.format(guy.IP, guy.ERA(), guy.WHIP(), guy.SO,  guy.W, guy.SV, guy.ADP)
        return (basic + full)
    
    def spgLine(self):
        ##self.xER()/self.spgxER + self.xWHIP()/self.spgxWHIP + self.SO/self.spgSO + self.W/self.spgW + self.SV/self.spgSV##
        basic = '{0:20} {1:10} {4:11} {2:6.2f} {3:5.2f} '.format(guy.name[0:17],team, guy.fWAR(), guy.fWAR150(), guy.printElig())
        #full = '   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:3.0f}  W {4:2.0f}  SV {5:2.0f}  ADP {6:6}'.format(guy.IP, self.xER()/self.spgxER, self.xWHIP()/self.spgxWHIP, self.SO/self.spgSO,  self.W/self.spgW, self.SV/self.spgSV, guy.ADP)
        full = "basic player has no stats"
        return (basic + full)
            


    @staticmethod
    def isaPitcher():
        return False
    
    @staticmethod
    def isReliever():
        return False

    @staticmethod
    def isaHitter():
        return False
    
    
