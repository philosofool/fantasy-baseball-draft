# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 09:23:35 2019

@author: sjl98
"""

##Quick valuator
from BaseClasses.Pitcher import Pitcher
from BaseClasses.Hitter import Hitter

def valuate():
    var = input("Hitter or pitcher?").lower()
    if var[0] == 'p':
        guy = PitcherValuer()
    else:
        guy = HitterValuer()
    print(guy.fWAR())

def main():
    keepgoing = True
    while keepgoing:
        valuate()
        a = input("Keep going? ").lower()
        if a[0] == 'n':
            keepgoing = False
        else:
            keepgoing = True

class PitcherValuer:
#    spgxER = 8.47# was in 2018, 7.85
#    spgSO = 17.47
#    spgW = 1.73
#    spgSV = 4.55
#    spgxWHIP = 10.848###was 10.60
#    lgERA = 3.79
#    lgWHIP = 1.23
#    replacementLevel = 11.44
    
    def __init__(self):
        self.getStandardValues()
        
    def getStandardValues(self):
        self.SO = self.getInput("K? ")
        self.ERA = self.getInput("ERA? ")
        self.WHIP = self.getInput("WHIP? ")
        self.W = self.getInput("W? ")
        self.SV = self.getInput("SV? ")
        self.IP = self.getInput("IP? ")
    
    @classmethod    
    def getInput(self,prompt):
        #print(prompt)
        var = input(prompt)
        return float(var.strip())
    
    def xER(self):
        return (Pitcher.lgERA - self.ERA)/9 * self.IP

    def xWHIP(self):
        return (Pitcher.lgWHIP - self.WHIP) * self.IP
    
    def fWAR(self):
        fWAR = self.xER()/Pitcher.spgxER + self.xWHIP()/Pitcher.spgxWHIP + self.SO/Pitcher.spgSO + self.W/Pitcher.spgW + self.SV/Pitcher.spgSV
        fWAR = fWAR - Pitcher.replacementLevel
        return fWAR
    
class HitterValuer(PitcherValuer):
    
    def __init__(self):
        self.getStandardValues()
        self.xH = (self.BA - Hitter.lgBA)*self.AB
    
    def getStandardValues(self):
        self.HR = self.getInput("HR? ")
        self.BA = self.getInput("BA? ")
        self.RBI = self.getInput("RBI? ")
        self.R = self.getInput("R? ")
        self.SB = self.getInput("SB? ")
        self.AB = self.getInput("AB? ")
        self.elig = dict()
        catcher = input("Is he a catcher? ")
        if catcher.lower()[0] == 'y':
            self.elig['C'] = True
        else:
            self.elig['C'] = False
        
        
    def fWAR(self):
        fWAR = self.HR/Hitter.spgHR + self.RBI/Hitter.spgRBI + self.R/Hitter.spgR + self.SB/Hitter.spgSB + self.xH/Hitter.spgxH# - self.replacementLevel
        if self.elig['C']:
            fWAR -= Hitter.catcherReplacement
        else:
            fWAR -= Hitter.replacementLevel
        ##print(fWAR)
        return fWAR       
    
main()