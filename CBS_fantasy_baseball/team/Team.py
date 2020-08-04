'''I'm trying to work out some bugs. This is just a copy of team and I want it to replace Team eventually.
--March 7, 2019
'''


from BaseClasses.player.Hitter import Hitter
from BaseClasses.player.Pitcher import Pitcher


def test():
    team = Team([])
    team.test()

    
class Team:
    '''a list of player objects. Reports on them as if that list composed a team.'''
    ##target scoring values

    targetBA = .273
    targetR = 837
    targetHR = 249
    targetRBI = 812
    targetSB = 117

    targetW = 81
    targetERA = 3.47
    targetSO = 1206
    targetWHIP = 1.17
    targetSV = 85
    targetIP = 1200

    spgxH = Hitter.spgxH
    spgHR = Hitter.spgHR
    spgR = Hitter.spgR
    spgRBI = Hitter.spgRBI
    spgSB = Hitter.spgSB
    lgBA = Hitter.lgBA
    hitterReplacementLevel = Hitter.replacementLevel

    spgxER = Pitcher.spgxER
    spgSO = Pitcher.spgSO
    spgW = Pitcher.spgW
    spgSV = Pitcher.spgSV
    spgxWHIP = Pitcher.spgxWHIP
    lgERA = Pitcher.lgERA
    lgWHIP = Pitcher.lgWHIP
    pitcherReplacementLevel = Pitcher.replacementLevel
    
    hittingString = "{0:5.0f} {1:5.3f}  {2:4} {3:3}  {4:4}  {5:3}"
    hittingStringHeader = "{0:>5} {1:>5}  {2:>4} {3:>3}  {4:>4}  {5:>3}".format("PA","BA","R","HR","RBI","SB")
    pitchingString = "{0:4} {1:4.2f}  {2:4.2f} {3:4}  {4:3}  {5:3}"
    pitchingStringHeader = "{0:4} {1:4}  {2:4} {3:4}  {4:3}  {5:3}".format("IP","ERA","WHIP","SO","W","SV")

    lineUpKeys = ['C','1B','2B','3B','SS','LF','RF','CF','IF', 'U','SP1','SP2','SP3','SP4','SP5','RP1','RP2','SP6', ]

    reportHitStr = "PA {0:5.0f}  BA {1:6.3f}  R {2:3.0f}  HR {3:3.0f}  RBI {4:3.0f}  SB {5:3.0f}; "
    reportPitchStr = "IP {0: >6.1f}  ERA {1:5.2f}  WHIP {2:5.2f} SO {3:4.0f}  W {4:3.0f}  SV {5:3.0f}"
    
    def __init__(self,players):
        self.name = str()
        self.players = []
        for player in players:
            self.append(player)
            
        self.pitchers = []
        self.hitters = []
        self.bench = []
        self.lineup = { 
                'C': None,
                '1B': None,
                '2B': None,
                '3B': None,
                'SS': None,
                'LF': None,
                'RF':None,
                'CF':None,
                'IF':None,
                'OF':None,
                'U':None,
                'SP1': None,
                'SP2': None,
                'SP3': None,
                'SP4': None,
                'SP5': None,
                'SP6':None,
                'RP1': None,
                'RP2': None,
                'SP7' : None,
                }
        
        
    def __iter__(self):
        return iter(self.players)
    
#    def __repr__(self):
#        return self.players
#    
#    def __str__(self):
#        return self
        
    def append(self,player):
        '''
        Adds players to the team. Use "addPlayer" to avoid redundant adds.
        '''
        try:
            player.isaHitter() or player.isaPitcher()
            if player not in self:
                self.players.append(player)
            else:
                print("Attempt to add {0} to {1} failed. {0} already on {1}".format(player,self))
        except AttributeError:
            raise TypeError("Object added to {} is type {}; must be instance of {} or {}".format(repr(self),type(player),Hitter,Pitcher))
    
    def reset(self):
        self.players = []
        self.hitters = []
        self.pitchers = []
        self.bench = []
        for pos in self.lineup:
            self.lineup[pos] = None
        
    def test(self,verbose = False):
        '''run this to check that the object is functional.'''
        print("...running test on {}".format(self))
        self.printPlayers()
        if not self.players:
            print("Players is empty. Using dummy players for test.")
            hitter1 = Hitter("Babe",150,600,500,100,70,30,5,45,90,90,6,2,100,"id100")
            hitter2 = Hitter("Jackie",150,600,500,100,80,30,5,15,90,90,25,2,50,"id101")
            pitcher1 = Pitcher("Sandy",16,7,32,32,0,200,200,70,10,200,40,"id201")
            pitcher2 = Pitcher("Bob",17,8,32,32,0,200,205,70,10,190,25,"id201")
            self.addPlayers([hitter1,hitter2,pitcher1,pitcher2])
            hitter1.addElig("C")
            hitter1.addElig("CF")
            hitter2.addElig("2B")
        self.setLineUp()
        self.printLineUp()
        print("Team Totals\n",self.TeamTotals())
        print("Team analysis\n",self.TeamAnalysis())

    def printPlayers(self):
        if len(self.players) == 0:
            print("{} is empty.".format(self))

    def clearLineUp(self):
        for pos in self.lineUpKeys:
            self.lineup[pos] = None
        self.hitters = []
        self.pitchers = []
        self.bench = []

    def setLineUp(self):
        '''specialized for KLF rules!'''
        #print("\n setSlineUp()")
        self.clearLineUp()
        self.players.sort(key=lambda guy: guy.fWAR(),reverse=True)
        temp = [] 
#        for guy in self.players:
#            temp.append(guy)##why is this? huh?
        #print(temp)
        positions = ['C','SS','CF','2B','3B','LF','RF','1B','CI','MI','OF','U']
        pitchers = []
        for i in self.lineup:
            if 'P' in i:
                pitchers.append(i)
        pitchers.reverse()
        self.hitters = []
        self.pitchers = []
        for guy in self.players:
            if guy.isaHitter() and guy not in self.hitters:
                for pos in positions:
                    if pos == 'CI' or pos == 'MI':
                        if guy.elig[pos]:
                            self.addToLineup(guy,'IF')
                            positions.remove('CI')
                            positions.remove('MI')
                            break
                    elif guy.elig[pos]:
                        if guy not in self.hitters:
                            self.hitters.append(guy)
                        self.lineup[pos] = guy
                        positions.remove(pos)
                        break
            elif guy.isaPitcher() and guy not in self.pitchers:
                try:
                    if pitchers:
                        self.addToLineup(guy,pitchers.pop())##pitcher.pop() returns a line up pitching position (SP4, e.g.)
                except Exception as err:
                    print("Exception on adding pitcher to line up.", err)
                    #pass#for now
        
        for guy in self.players:
            if guy not in self.hitters and guy not in self.pitchers:
                self.bench.append(guy)
        
        positions = ['C','SS','CF','2B','3B','LF','RF','1B','CI','MI','OF','U']        
#        for scrub in self.bench:##now check to see if a multi-eligible guy got benched.
#            for hitter in self.hitters:
#                if scrub.fWAR() > hitter.fWAR():
#                    for pos in positions:
#                        if scrub.elig[pos] and hitter.elig[pos]:
#                            self.lineup[pos] = scrub
#                            self.hitters.remove(hitter)
#                            self.hitters.append(scrub)
#                            self.bench.append(hitter)
        lineupTests = 0##for breaking the while loop below        
        while self.hasHittersOnBench() and not self.lineupComplete():
            lineupTests += 1
            if lineupTests > 100:
                break##end the while loop if this is lasting too long.
            checked = set()
            for pos in self.emptyPositions():
                if self.hasHitterEligAt(pos):
                    for guy in self.hitters:
                        try:
                            if guy.elig[pos]:
                                elig = True
                            else:
                                elig = False
                        except:
                            elig = False
                        if elig and guy not in checked:
                            checked.add(guy)
                            self.removeFromLineup(guy)
                            for dude in self.bench:
                                try:
                                    if dude.elig[pos]:
                                        self.addToLineup(guy,pos)
                                        break
                                except KeyError:
                                    if dude.isaPitcher():
                                        pass
                                    else:
                                        print(dude)
                                        print("Weird exception. Moving on.",err)
                            break
            self.bench.sort(key = lambda guy:guy.fWAR(),reverse = True)
            breakTime = False
            for pos in self.emptyPositions():
                if self.hasBenchEligAt(pos):
                    for guy in self.bench:
                        if guy.elig[pos]:
                            self.addToLineup(guy,pos)
                            break
            for pos in self.emptyPositions():
                    if not self.hasBenchEligAt(pos):
                        breakTime = True
                        break
            if breakTime:
                break
        self.bench.sort(key = lambda guy:guy.isaHitter())

    
    def hasBench(self):
        if self.bench:
            return True
        else:
            return False

    def hasHittersOnBench(self):
        for guy in self.bench:
            if guy.isaHitter():
                return True
        return False

        
    def hasPlayerEligAt(self,pos):
        for guy in self.players:
            if guy.elig[pos]:
                return True
        return False

    def hasHitterEligAt(self,pos):
        '''only looks at hitters in the lineup!'''
        for guy in self.hitters:
            if pos == "IF":
                if guy.elig["CI"] or guy.elig["MI"]:
                    return True
            elif guy.elig[pos]:
                return True
        return False
    
    def hasBenchEligAt(self,pos):
        for guy in self.bench:
            if guy.isaHitter():
                
                try:
                    if guy.elig[pos]:
                        return True
                except:
                    print("I have no idea why hasBenchEligAt' raised and exception.")
        return False
    
    def lineupComplete(self):
        for pos in self.lineUpKeys:
            if self.lineup[pos] == None:
                return False
        return True

    @staticmethod
    def targetStats():
        outstring = "{:5} {:4} {:4} {:3} {:4} {:4} {:4} {:4} {:4} {:4} {:4}"
        a = outstring.format("BA","R","HR","RBI","SB","IP","W","ERA","WHIP","SO","SV")
        b = outstring.format(
            Team.targetBA,
            Team.targetR,
            Team.targetHR,
            Team.targetRBI,
            Team.targetSB,
            Team.targetIP,
            Team.targetW,
            Team.targetERA,
            Team.targetWHIP,
            Team.targetSO,
            Team.targetSV
            
            )
        return(a+"\n"+b)

    
    def emptyPositions(self):
        positions = ['C','SS','CF','2B','3B','LF','RF','1B','IF','OF','U']
        out = []
        for pos in positions:
            if self.lineup[pos] == None:
                out.append(pos)
        return out
                        

    def printLineUp(self):
        out = ""
        for pos in self.lineup:
            guy = self.lineup[pos]
            #print(guy.assistLine())
            try:
                out += "{:3} {}\n".format(pos, guy.assistLine())
            except:##if the guy is still None type, print "None" for the unassigned positions
                
                out +="{:3} {}\n".format(pos, None)
        for guy in self.bench:
            out += "{:3} {}\n".format("Res", guy.assistLine())
        return out

    def HR(self):
        HR = 0
        for guy in self.hitters:
            if guy.isaHitter():
                HR = HR + guy.HR
        return HR

    def RBI(self):
        RBI = 0
        for guy in self.hitters:
            if guy.isaHitter():
                RBI = RBI + guy.RBI
        return RBI


    def R(self):
        R = 0
        for guy in self.hitters:
            if guy.isaHitter():
                R = R + guy.R
        return R

    def SB(self):
        SB = 0
        for guy in self.hitters:
            if guy.isaHitter():
                SB = SB + guy.SB
        return SB

    def BA(self):
        try:
            H = 0
            AB = 0
            for guy in self.hitters:
                if guy.isaHitter():
                    H = H + guy.calcHits()
                    AB = AB + guy.AB
            return  H/AB
        except ZeroDivisionError:
            return 0.0

    def PA(self):
        x = 0
        for guy in self.hitters:
            #print(guy.name)
            if guy.isaHitter():
                x = x + guy.PA
        return x

    def AB(self):
        x = 0
        for guy in self.hitters:
            if guy.isaHitter():
                x = x + guy.AB
        return x

    def IP(self):
        x = 0
        for guy in self.pitchers:
            if guy.isaPitcher():
                x = x + guy.IP
        return x

    def SO(self):
        x = 0
        for guy in self.pitchers:
            if guy.isaPitcher():
                x = x + guy.SO
        return x
        
    def W(self):
        x = 0
        for guy in self.pitchers:
            if guy.isaPitcher():
                x = x + guy.W
        return x

    def SV(self):
        x = 0
        for guy in self.pitchers:
            if guy.isaPitcher():
                x = x + guy.SV
        return x

    def ERA(self):
        x = 0
        try:
            for guy in self.pitchers:
                if guy.isaPitcher():
                    x = x + guy.ER
            return x/self.IP()*9
        except ZeroDivisionError:
            return 0.0

    def WHIP(self):
        x = 0
        try:
            for guy in self.pitchers:
                if guy.isaPitcher():
                    x = x + guy.BB + guy.H
            return x/self.IP()
        except ZeroDivisionError:
            return 0.0
    
    def addAPlayer(self,player):
        if player not in self:
            self.append(player)        
    
    def addPlayers(self,playerlist):
        for guy in playerlist:
            self.addAPlayer(guy)
            
    def removePlayer(self,player):
        self.players.remove(player)
        if player in self.pitchers:
            self.pitchers.remove(player)
        if player in self.hitters:
            self.hitters.remove(player)
        if player in self.bench:
            self.bench.remove(player)
        for key in self.lineUpKeys:
            if self.lineup[key] == player:
                self.lineup[key] = None
                           
    def addToLineup(self,guy,pos):
        '''adds a guy to your lineup and removes from bench. 
        Note: may cause errors while itterating over self.bench!'''
        self.lineup[pos] = guy
        if guy.isaPitcher():
            if guy not in self.pitchers:
                self.pitchers.append(guy)
            
        else:
            if guy not in self.hitters:
                self.hitters.append(guy)
        if guy in self.bench:
            self.bench.remove(guy)
            
    def removeFromLineup(self,guy):
        '''removes a guy from your lineup and cleans up pitchers, hitters, etc.'''
        for pos in self.lineUpKeys:
            if self.lineup == guy:
                self.lineup[pos] == None
                break
        if guy not in self.bench:
            self.bench.append(guy)
        if guy.isaPitcher():
            self.pitchers.remove(guy)
        else:
            self.hitters.remove(guy)

    def teamTotals(self):
        hitting = (self.reportHitStr.format(int(self.PA()), self.BA(), self.R(), self.HR(), self.RBI(), self.SB()))
        pitching = (self.reportPitchStr.format(self.IP(), self.ERA(), self.WHIP(), self.SO(), self.W(), self.SV()))
        return(hitting + pitching)

    def teamAnalysis(self):
        '''Returns the difference between target and desired rate.'''
        ba = self.targetBA - self.BA()
        hr = self.targetHR - self.HR()
        r = self.targetR - self.R()
        rbi = self.targetRBI - self.RBI()
        sb = self.targetSB - self.SB()

        ip = self.targetIP - self.IP()
        so = self.targetSO - self.SO()
        era = self.targetERA - self.ERA()
        whip = self.targetWHIP - self.WHIP()
        w = self.targetW - self.W()
        sv = self.targetSV - self.SV()
        
        hitting = (self.reportHitStr.format(self.PA(), ba, r, hr, rbi, sb))
        pitching = (self.reportPitchStr.format(ip, era, whip, so, w, sv))
        return (hitting + pitching)

    def teamSPGAnalysis(self):
        ''' How many stnadings points needed based on SPG numbers.'''
        ba = (self.BA() - self.targetBA)*self.AB()/self.spgxH
        hr = (self.targetHR - self.HR())/self.spgHR
        r = (self.targetR - self.R())/self.spgR
        rbi = (self.targetRBI - self.RBI())/self.spgRBI
        sb = (self.targetSB - self.SB())/self.spgSB

        ip = self.targetIP - self.IP()
        so = (self.targetSO - self.SO())/self.spgSO
        era = (self.ERA() - self.targetERA)*self.IP()/9/self.spgxER
        whip = (self.WHIP() - self.targetWHIP)*self.IP()/self.spgxWHIP
        w = (self.targetW - self.W())/self.spgW
        sv = (self.targetSV - self.SV())/self.spgSV
        
        hitting = (self.reportHitStr.format(self.PA(), ba, r, hr, rbi, sb))
        pitching = (self.reportPitchStr.format(ip, era, whip, so, w, sv))
        return (hitting + pitching)

    def teamPerGuyAnalysis(self):
        hitters = 0
        pitchers = 0
        for guy in self:
            if guy.isaHitter():
                hitters += 1
            elif guy.isaPitcher():
                pitchers += 1
        
        ba = (self.targetBA - self.BA())/hitters
        hr = (self.targetHR - self.HR())/hitters
        r = (self.targetR - self.R())/hitters
        rbi = (self.targetRBI - self.RBI())/hitters
        sb = (self.targetSB - self.SB())/hitters

        ip = (self.targetIP - self.IP())/pitchers
        so = (self.targetSO - self.SO())/pitchers
        era = (self.targetERA - self.ERA())/pitchers
        whip = (self.targetWHIP - self.WHIP())/pitchers
        w = (self.targetW - self.W())/pitchers
        sv = (self.targetSV - self.SV())/pitchers
        
        hitting = (self.reportHitStr.format(self.PA(), ba, r, hr, rbi, sb))
        pitching = (self.reportPitchStr.format(ip, era, whip, so, w, sv))
        return (hitting + pitching)
    
        
    
    @staticmethod
    def assistLineHitter(guy):
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        basic = '{0:20} {1:10} {2:11} {3:5.2f} {4:5.2f} '.format(guy.name[0:17],team, guy.printElig(), guy.fWAR(), guy.fWAR600())
        full = '   PA {5:3.0f}  BA {0:.3f}  RBI {1:3.0f}  R {2:3.0f}  HR {3:2.0f}  SB {4:2.0f}'.format(guy.BA(), guy.RBI, guy.R, guy.HR, guy.SB, guy.PA)
        return (basic + full)
        
    @staticmethod
    def assistLinePitcher(guy):
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        basic = '{0:20} {1:10} {4:11} {2:5.2f} {3:5.2f}'.format(guy.name[0:17],team, guy.fWAR(), guy.fWAR150(), guy.printElig())
        full = '   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:3.0f}  W {4:2.0f}  SV {5:2.0f}'.format(guy.IP, guy.ERA(), guy.WHIP(), guy.SO,  guy.W, guy.SV)
        return (basic + full)




if __name__ == "__main__":    
    test()
##main()
