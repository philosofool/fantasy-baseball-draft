import csv
from copy import deepcopy
from .Player import Player


class Hitter(Player):

    spgxH = 8.475##used 8.47, nearly matched the real value of 8.486 in 2019.
    spgHR = 5.286##real value was 4.782
    spgR = 11.671###used 10.81,real value was 12.532
    spgRBI = 13.38##used 12.20,was 14.564
    spgSB = 3.46##used 4.27,was 2.657
    lgBA = .265
    replacementLevel = 16.72
    catcherReplacement = 9##This is an approximation. Draft assistant has methods for finding it in a list

    
    def __init__(self, name, G, PA, AB, BB, H1B, H2B, H3B, HR, R, RBI, SB, CS, SO, playerID):
        try: ##verify the data is proper type:
            (G + PA + AB + H1B + H2B + H3B + HR + R + RBI + SB + CS + SO)
        except ValueError:
            raise ValueError("This object {} {} was created with non integer types for numerical variables.".format(self,name))
            
        self.name = name
        self.Games = G
        self.PA = PA
        self.AB = AB
        self.BB = BB
        self.H1B = H1B
        self.H2B = H2B
        self.H3B = H3B
        self.HR = HR
        self.R = R
        self.RBI = RBI
        self.SB = SB
        self.CS = CS
        self.SO = SO
        self.playerID = playerID
        self.hits = self.calcHits()
        self.elig = {
            'C'  : False,
            '1B' : False,
            '2B' : False,
            '3B' : False,
            'SS' : False,
            'RF' : False,
            'CF' : False,
            'LF' : False,
            'DH' : False,
            'MI' : False,
            'CI' : False,
            'OF' : False,
            'U'  : True
            }
        
        self.avail = True
        self.team = None
        
    def __str__(self):
        return "Hitter {}".format(self.name)
    
    def __repr__(self):
        return "Hitter {}".format(self.name)
    

    def printPlayer(self):
        '''this just prints all the basic stats for a player, helps to see that data is right.'''
        print(
        self.name,
        self.PA,
        self.AB,
        self.BB,
        self.H1B,
        self.H2B,
        self.H3B,
        self.HR,
        self.R,
        self.RBI,
        self.SB,
        self.CS,
        self.SO,
        self.playerID,
        self.hits

            )

    def adjToPA(self,PA):
        try:
            self.formerPA = self.PA
            ratio = PA/self.PA
            self.PA = self.PA * ratio
            self.AB = self.AB * ratio
            self.BB = self.BB * ratio
            self.H1B = self.H1B  * ratio
            self.H2B = self.H2B  * ratio
            self.H3B = self.H3B  * ratio
            self.HR = self.HR  * ratio
            self.R = self.R  * ratio
            self.RBI = self.RBI  * ratio
            self.SB = self.SB  * ratio
            self.CS = self.CS  * ratio
            self.SO = self.SO  * ratio
            self.hits = self.calcHits()
        except ZeroDivisionError:
            pass
        
    def asNumberPA(self,pa):
        guy = deepcopy(self)
        guy.adjToPA(pa)
        return guy
            
        
        
        
    def calcHits(self):
        output = self.H1B + self.H2B + self.H3B + self.HR
        return output


        

    def TB(self):
        return self.H1B + 2*self.H2B + 3*self.H3B + 4*self.HR

    def SLG(self):
        try:
            return self.TB()/self.AB
        except ZeroDivisionError:
            return 0

    def BA(self):
        try:
            return self.hits/self.AB
        except ZeroDivisionError:
            return 0

    def OBP(self):
        try:
            return (self.hits + self.BB)/(self.AB + self.BB)
        except ZeroDivisionError:
            return 0
    
    def calcxH(self):
        self.xH = (self.BA()-self.lgBA)*self.AB
        return self.xH
        
    def fWAR(self):
        fWAR = self.HR/self.spgHR + self.RBI/self.spgRBI + self.R/self.spgR + self.SB/self.spgSB
        self.xH = self.calcxH()
        fWAR = fWAR + self.xH/self.spgxH# - self.replacementLevel
        if self.elig['C']:
            fWAR -= self.catcherReplacement
        else:
            fWAR -= self.replacementLevel
        ##print(fWAR)
        return fWAR

    def rawWAR(self):
        '''Returns fWAR without replacement level adjustment.'''
        fWAR = self.HR/self.spgHR + self.RBI/self.spgRBI + self.R/self.spgR + self.SB/self.spgSB
        self.xH = self.calcxH()
        fWAR = fWAR + self.xH/self.spgxH ## - self.replacementLevel
        #if self.elig['C']:
        #    fWAR = fWAR +(16.72-12.59)
        ##print(fWAR)
        return fWAR


    def fWAR600(self):
        PA = self.PA
        try:
            try:
                if player.elig['C']:
                    self.adjToPA(450)
                    fWAR600 = self.rawWAR()
                    self.adjToPA(PA)
                else:
                    self.adjToPA(600)
                    fWAR600 = self.rawWAR()
                    self.adjToPA(PA)
            except:
                self.adjToPA(600)
                fWAR600 = self.rawWAR()
                self.adjToPA(PA)
        except ZeroDivisionError:
            fWAR600 = None
        
        return fWAR600

    def addElig(self, pos):
        self.elig[pos]=True
                 
    def multiEligible(self):
        positions = ['C','1B','2B','3B','SS','RF','CF','LF']
        num = 0
        for pos in positions:
            if self.elig[pos]:
                num += 1
        if num >1:
            return True
        else:
            return False
                 
    def eligAt(self):
        s = str()
        for key in self.elig:
            if self.elig[key]:
                s = s + " " + key
        return s

    def assistLine(self):
        guy = self
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        try:
            ADP = guy.ADP
        except:
            ADP = 0
        basic = '{0:20} {1:10} {2:11} {3:6.2f} {4:5.2f} '.format(guy.name[0:17],team, guy.printElig(), guy.fWAR(), guy.fWAR600())
        full = '   PA {5:3.0f}  BA {0:.3f}  RBI {1:3.0f}  R {2:3.0f}  HR {3:2.0f}  SB {4:2.0f}   ADP {6:6}'.format(guy.BA(), guy.RBI, guy.R, guy.HR, guy.SB, guy.PA, ADP)
        return (basic + full)

    

    @staticmethod
    def isaHitter():
        return True

