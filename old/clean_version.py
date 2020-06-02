'''
This is all about writing a writing something that can
-run with my draft assistant script
-make a (bunch of?) projections .csv files for me.
'''



import csv
from BaseClasses.Hitter import Hitter
from BaseClasses.Pitcher import Pitcher
from BaseClasses.BaseFantasyClasses import FansHitters
from BaseClasses.BaseFantasyClasses import HitterFile
from BaseClasses.BaseFantasyClasses import FanPitcherFile
from BaseClasses.BaseFantasyClasses import DepthPitcherFile
from BaseClasses.BaseFantasyClasses import CBSFilePlayers



def test():
    file = open('FGDepthProjections2017.csv', 'r')
    file = csv.reader(file, delimiter =',', quotechar= '"')
    print(file.next())
    print(file.readline())
    print(file.readline())
    
    main = HitterFile("FG_depth_hitters.csv")#create hitter objects from fangraphs file
    a = hittingStuff()
    pitchingStuff()
    print(a[2].name)
    
def hittingStuff(hitterProjections):
    '''returns a list of hitter objects, adjusted for position. hitterProjections has been
    a fangraphs depthchart projections file in the past'''
    
    ##main = HitterFile("FG_depth_hitters.csv")#create hitter objects from fangraphs file
    main = HitterFile(hitterProjections)#("FGDepthProjections2017.csv")#create hitter objects from fangraphs file
    cbsData = CBSFilePlayers("Files/elig_testing.csv")#create a list of players from CBS files
    fans = FansHitters("Fans/all_hitters.csv")#create a list of 
##    firstbase = FansHitters("Fans/firstbase.csv")
##    secondbase = FansHitters("Fans/secondbase.csv")
##    thirdbase = FansHitters("Fans/thirdbase.csv")
##    shortstop = FansHitters("Fans/shortstop.csv")
##    rightfield = FansHitters("Fans/rightfield.csv")
##    centerfield = FansHitters("Fans/centerfield.csv")
##    leftfield = FansHitters("Fans/leftfield.csv")
##    designatedhitter = FansHitters("Fans/designatedhitter.csv")
    
    main.sort(key=lambda hitter: hitter.playerID)
    ##print(cbsData.repeatedPlayerNames)


    '''Assign players CBS eligibility'''
    for player in main:
        for guy in cbsData:
            if guy.name == player.name:
                if guy.name in cbsData.repeatedPlayerNames:
                    pass
                else:
                    for key in guy.elig:
                        if key == "U":
                            pass
                        else:                            
                            player.elig[key] = True

    
    
    ##assign eligibility to hitters and adjust RBIs and R by fans projections.

    



    for hitter in main:
        for guy in fans:
            if guy.playerID == hitter.playerID:
                #hitter.adjToPA(guy.PA)
                hitterRBI = averageRBI(hitter,guy)
                hitterR = averageR(hitter,guy)
                break



    ## determine some replacement levels.
    repAll = []
    repC = []
    repSS = []
    repCF = []

    ##Hitter.replacementLevel = 16.68
    ##print("Determining Replacment Levels")##you actually need to do this manually
    personalTouch(main)


    ##print(repAll[-165],repCF[-15],repSS[-15], repC[-15])
    Hitter.replacementLevel = main.replacementLevel()
    #print("Hitter replacement level: {:.5}".format(main.replacementLevel()))
    
    return main

def pitchingStuff(pitchers="FG_depth_pitchers.csv"):
    '''returns a list of pitcher objects.'''
    ##pitchers next
    mainPitchers = DepthPitcherFile(pitchers)
    fanPitchers = FanPitcherFile("Fans/pitcher.csv")
    mainPitchers.sort(key=lambda pitcher: pitcher.playerID)

    Pitcher.replacementLevel = mainPitchers.replacementLevel()


    personalTouch(mainPitchers)
    return mainPitchers

def writeProj(hitters,pitchers,outfile):
    ##print("Writing projections file...")
    myProj = Projections(outfile,hitters,pitchers)
    myProj.writeRows()

    ##print("Projections written to ", myProj.file)
    
                
def personalTouch(guys):
    ''' This is where I change some guys stats because Steamer is wrong. Like Joey Votto is not a .283 hitter.'''

    for guy in guys:
        if guy.playerID == "11003":##Evan Gattis
            ##print(guy.name, "is not a catcher...")
            ###peronal touch here....
            guy.elig['C']=False
        if guy.playerID == "sa597765":##Trevor Story
            guy.elig['SS'] = True

        if guy.playerID == "3142":##Robinson Chirinos
            guy.elig['C'] = True

        
def averageIP(guy1,guy2):
    return guy1.IP*.5 + guy2.IP*.5

def averageSV(guy1,guy2):
    IP = guy1.IP
    guy2.adjToIP(IP)
    out = guy2.SV
                    
        
def averageRBI(guy1,guy2):
    ##print(guy1.RBI, type(guy1.RBI))
    ratio = guy1.PA/guy2.PA
    RBI1 = guy1.RBI - guy1.HR
    RBI2 = (guy2.RBI - guy2.HR)*ratio
    return (RBI1 + RBI2)/2 + guy1.HR

def averageR(guy1, guy2):
    ratio = guy1.PA/guy2.PA
    R1 = guy1.R - guy1.HR
    R2 = ratio*(guy2.R - guy2.HR)
    return (R1 + R2)/2 + guy1.HR
                

    

class Projections:
    '''basically just writes results to a file.'''
    def __init__(self,file,hitters,pitchers):
        self.header = ["Name", "Pos","PA/IP", "BA","R","HR","RBI","SB","ERA","WHIP","W","SO","SV","fWAR","fWAR600"]
        ##mainPitchers.pitchers.sort(key=lambda pitcher: pitcher.playerID)
        pitchers.sort(key=lambda pitcher: pitcher.fWAR())
        hitters.sort(key=lambda hitter: hitter.fWAR())
        self.pitchers = pitchers
        self.hitters = hitters
        self.file = file

    def writeRows(self):
        with open(self.file, 'w', newline='') as csvfile:
            projections = csv.writer(csvfile, delimiter = ',',quotechar='"')
            
            projections.writerow(self.header)
            for hitter in self.hitters:
                projections.writerow(self.hitterData(hitter))
            for pitcher in self.pitchers:
                projections.writerow(self.pitcherData(pitcher))

    def hitterData(self, hitter):
        temp = ""
        for key in hitter.elig:
            if hitter.elig[key]:
                temp = temp + key + " "
        out = [hitter.name,hitter.playerID,temp,hitter.PA,round(hitter.BA(),3),hitter.R,hitter.HR,hitter.RBI,hitter.SB,'','','','','',hitter.fWAR(),hitter.fWAR600()]
        return out

    def pitcherData(self,pitcher):
        out = [pitcher.name,pitcher.playerID,"P",pitcher.IP,'','','','','',round(pitcher.ERA(),2),round(pitcher.WHIP(),2),pitcher.W,pitcher.SO,pitcher.SV,pitcher.fWAR(),pitcher.fWAR150()]
        return out

    



##test()
##closers()
##main()
##hittingStuff()
