

'''

This thing worked pretty well. We'll see if the base system is a good one.
That's more of an issue with the underlying model, though. I really liked
how this worked.

Known Issues:
-Fangraphs Eligibility was not 100%. :: Fixed March 30

-You need the power to exclude players based on eligibility: i.e,
don't show any CI guys right now. 

'''

from clean_version import hittingStuff
from clean_version import pitchingStuff

import myTeam

from BaseFantasyClasses import Pitcher
from BaseFantasyClasses import Hitter
from BaseFantasyClasses import SimplePlayer
from BaseFantasyClasses import CBSFilePlayers

import csv


    

def main():
    hitters = CBSFilePlayers("Files/stats-main.csv")
    pitchers = CBSFilePlayers("Files/projections.csv")
    myHitterProj = hittingStuff()
    myPitcherProj = pitchingStuff()

    print("GUY ",hitters.playersAtPosition("SS")[1].name)

    
    ##myTeam.main()
                      
    posFilter = False ##False means none, a string means matches a string.
    closersOnly = False ##False means print all pitchers, True means guys projected to get saves only
    showRookies = False ##prints rookies of note, if available
    showLiked = False ##prints guys I like, if available
    upside = False ## False sorts by fWAR, True sorts by fWAR/PA or IP.
    upsideMinPA = 150
    upsideMinIP = 30

    badGuys = [ ##Add the name of anyone you want to exclude here.
        "Jose Fernandez",##there are some other ones...
        "Matt Duffy"
        ]

##DON'T Erase Below!!! Can be used to adjust SPG during draft.

    ##Hitter.spgxH = 9.20
    ##Hitter.spgHR = 3.75 ##3.75
    ##Hitter.spgR = 11.32
    ##Hitter.spgRBI = 8.48
    ##Hitter.spgSB = 3.0 ##4.49
    ##Hitter.lgBA = .270
    ##Hitter.replacementLevel = 16.72

##    Pitcher.spgxER = 7.85
##    Pitcher.spgSO = 12.99
##    Pitcher.spgW = 1.59 
##    Pitcher.spgSV = 5.19
##    Pitcher.spgxWHIP = 10.60
##    Pitcher.lgERA = 3.5
##    Pitcher.lgWHIP = 1.21
##    Pitcher.replacementLevel = 11.44

#    Hitter.replacementLevel = myHitterProj[164].rawWAR()
#    Pitcher.ReplacementLevel = myPitcherProj[130].rawWAR()

    
    availHitters = []
    availPitchers = []
    likedIDs = guysILike()
    liked = []
    rookieIDs = interestingRookies()
    rookies = []
    
    for player in hitters:
        for guy in myHitterProj:
                
            if guy.name == player.name:
                if guy.name in badGuys:
                    pass #ignore this player
                else:
                    if not posFilter:
                        availHitters.append(guy)
                    elif guy.elig[posFilter]:
                        availHitters.append(guy)
                    
                if guy.playerID in likedIDs:
                    liked.append(guy)
                if guy.playerID in rookieIDs:
                    rookies.append(guy)

                    
    for player in pitchers:
        for guy in myPitcherProj:
            if guy.name == player.name:
                if guy.name in badGuys:
                    pass  #ignore this player
                else:
                    if guy.playerID in likedIDs:
                        liked.append(guy)
                    if guy.playerID in rookieIDs:
                        rookies.append(guy)
                    if not closersOnly:
                        availPitchers.append(guy)
                    elif guy.hasSaves():
                        availPitchers.append(guy)
    if not upside:
        availHitters.sort(key=lambda hitter: hitter.fWAR(), reverse = True)
        availPitchers.sort(key=lambda pitcher: pitcher.fWAR(), reverse = True)
    else:
        print("\n Players sorted by fWAR/play time rate stat.")
        availHitters.sort(key=lambda hitter: hitter.fWAR600(), reverse = True)
        availPitchers.sort(key=lambda pitcher: pitcher.fWAR150(), reverse = True)
        
    liked.sort(key=lambda player: player.fWAR(), reverse = True)

    print("\n")

    if upside:
        n = 0
        for guy in availHitters:
            if n <= 8:
                if guy.PA >= upsideMinPA:
                    assistLineHitter(guy)
                    n = n + 1
            else:
                break
            
            
    else:
        for guy in availHitters[0:8]:
            assistLineHitter(guy)

    print("\n")
    if upside:
        n = 0
        for guy in availPitchers:
            if n <= 8:
                if guy.IP > upsideMinIP:
                    assistLinePitcher(guy)
                    n = n + 1
                elif guy.SV > 0:
                    assistLinePitcher(guy)
                    n = n + 1
            else:
                break
        
    else:
        for guy in availPitchers[0:8]:
            assistLinePitcher(guy)

    if showLiked:
        print("\n Guys I like:")
        for guy in liked:
            if guy.isaHitter():            
                assistLineHitter(guy)
            else:
                assistLinePitcher(guy)
        print("John Lamb is your mother fuckin' DL guy!")
        print("Jumbo and Cingrani are cuffs for Hoover.")


    if showRookies:
        print("Rookies....")
        for guy in rookies:
            if guy.isaHitter():            
                assistLineHitter(guy)
            else:
                assistLinePitcher(guy)



                
def test():
    hitters = CBSFilePlayers("Files/elig_testing.csv")
    ##print(hitters.names()[0:10])
    names = hitters.names()
    print(names[0:3])
    print('CF' in hitters[1].elig)


def guysILike():
    '''add fangraphs player id's for guys I like, return as list'''
    guysILike = []

    guysILike.append("sa657852")##Jose Berios, rookie pitcher
    guysILike.append("sa597835")##Tyler Glasnow
    guysILike.append("sa657908")##Lucas Giolitto
    guysILike.append("8493")##John Lamb
    guysILike.append("12799")##Cody Anderson
    guysILike.append("7836")##Strickland

    
    guysILike.append("5297")##Arron Hicks
    guysILike.append("12533")##Marcus Semien
    guysILike.append("12979")##Javy Baez
    guysILike.append("12944")##Socrates Brito!
    guysILike.append("sa597765")##Trevor Story
    guysILike.append("14161")##Byron Buxton
    guysILike.append("10071")##Jonathan Villar
    ##guysILike.append("11476")##Odubel Herrera
    
    return guysILike


def interestingRookies():
    '''add fangraphs player id's for rookies I like, return as list'''
    rookies = []
    ##rookies.append()##
    return rookies
    

def assistLineHitter(guy):
    team = guy.team
    if team == "Diamondbacks":
        team = "Dbacks"
    basic = '{0:20} {1:10} {2:11} {3:5.2f} {4:5.2f} '.format(guy.name,team, printElig(guy), guy.fWAR(), guy.fWAR600())
    full = '   PA {5:3.0f}  BA {0:.3f}  RBI {1:3.0f}  R {2:3.0f}  HR {3:2.0f}  SB {4:2.0f}'.format(guy.BA(), guy.RBI, guy.R, guy.HR, guy.SB, guy.PA)
    print(basic + full)
    
def assistLinePitcher(guy):
    team = guy.team
    if team == "Diamondbacks":
        team = "Dbacks"
    basic = '{0:20} {1:10} {4:11} {2:5.2f} {3:5.2f}'.format(guy.name,team, guy.fWAR(), guy.fWAR150(), "P")
    full = '   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:3.0f}  W {4:2.0f}  SV {5:2.0f}'.format(guy.IP, guy.ERA(), guy.WHIP(), guy.SO,  guy.W, guy.SV)
    print(basic + full)

def printElig(guy):
    out = []
    for i in guy.elig:
        if guy.elig[i]:
            out.append(i)
    return ",".join(out)


        

##test()
main()
