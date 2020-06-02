import csv

def test():
    ##b = FanPitcherFile("Fans/pitcher.csv")
    test = Defensive("2015_defenders.csv")
    print(test[1].pos)



    
def main():
    main = HitterFile("SteamerHitters_2016.csv")
    catcher = FansHitters("Fans/catcher.csv")
    firstbase = FansHitters("Fans/firstbase.csv")
    secondbase = FansHitters("Fans/secondbase.csv")
    thirdbase = FansHitters("Fans/thirdbase.csv")
    shortstop = FansHitters("Fans/shortstop.csv")
    rightfield = FansHitters("Fans/rightfield.csv")
    centerfield = FansHitters("Fans/centerfield.csv")
    leftfield = FansHitters("Fans/leftfield.csv")
    designatedhitter = FansHitters("Fans/designatedhitter.csv")

    ##pitchers next
    mainPitchers = SteamerPitcherFile("steamer_pitchers_2016.csv")
    fanPitchers = FanPitcherFile("Fans/pitcher.csv")

    mainPitchers.pitchers.sort(key=lambda pitcher: pitcher.playerID)
    main.hitters.sort(key=lambda hitter: hitter.playerID)
    
    ##assign eligibility to hitters and adjust RBIs and R by fans projections.
    for hitter in catcher.hitters:
        hitter.addElig('C')
    for hitter in firstbase.hitters:
        hitter.addElig('1B')
    for hitter in secondbase.hitters:
        hitter.addElig('2B')
    for hitter in thirdbase.hitters:
        hitter.addElig('3B')
    for hitter in shortstop.hitters:
        hitter.addElig('SS')
    for hitter in rightfield.hitters:
        hitter.addElig('RF')
    for hitter in centerfield.hitters:
        hitter.addElig('CF')
    for hitter in leftfield.hitters:
        hitter.addElig('LF')

    examined = set()##lists playerIDs that have been adjusted.
    print("Adjusting hitter values...")
    for hitter in main.hitters:
        for guy in catcher.hitters:
            if guy.playerID == hitter.playerID:
                hitter.adjToPA(guy.PA)
                hitterRBI = averageRBI(hitter,guy)
                hitterR = averageR(hitter,guy)
                hitter.addElig('C')
                examined.add(hitter.playerID)
        for guy in firstbase.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('1B')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('1B')
                    examined.add(hitter.playerID)
        
        for guy in secondbase.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('2B')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('2B')
                    examined.add(hitter.playerID)
        for guy in thirdbase.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('3B')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('3B')
                    examined.add(hitter.playerID)
        
        for guy in shortstop.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('SS')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('SS')
                    examined.add(hitter.playerID)
        
        for guy in rightfield.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('RF')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('RF')
                    examined.add(hitter.playerID)
        
        for guy in centerfield.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('CF')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('CF')
                    examined.add(hitter.playerID)
        
        for guy in leftfield.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('LF')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('LF')
                    examined.add(hitter.playerID)
        
        for guy in designatedhitter.hitters:
            if guy.playerID == hitter.playerID:
                if guy.playerID in examined:
                    hitter.addElig('DH')
                else:
                    hitter.adjToPA(guy.PA)
                    hitterRBI = averageRBI(hitter,guy)
                    hitterR = averageR(hitter,guy)
                    hitter.addElig('DH')
                    examined.add(hitter.playerID)
                    
    ## add posotions based on last year

    defenders = Defensive("2015_defenders.csv")
    for player in defenders:
        for guy in main.hitters:
            if guy.playerID == player.playerID:
                guy.addElig(player.pos)
                


    ## determine some replacement levels.
    repAll = []
    repC = []
    repSS = []
    repCF = []

    ##Hitter.replacementLevel = 16.68
    print("Determining Replacment Levels")##you actually need to do this manually
    for hitter in main.hitters:
        repAll.append(hitter.fWAR())
        if hitter.elig['C']:
            repC.append(hitter.fWAR())
        if hitter.elig['SS']:
            repSS.append(hitter.fWAR())
        if hitter.elig['2B']:
            repCF.append(hitter.fWAR())

    repAll.sort()
    repC.sort()
    repSS.sort()
    repCF.sort()

    ##print(repAll[-165],repCF[-15],repSS[-15], repC[-15])

    ##let's fix up the pitchers.
    print("Adjusting pitcher values...")
    for pitcher in mainPitchers.pitchers:
        for guy in fanPitchers.pitchers:
            if pitcher.playerID == guy.playerID:
                temp = averageIP(pitcher,guy)
                pitcher.adjToIP(temp)
                temp = averageSV(pitcher,guy)
                examined.add(pitcher.playerID)
                break

    ##Write the file!!!

    print("Adding personal touches....")

    personalTouch(mainPitchers.pitchers)
    personalTouch(main.hitters)

    print("Writing projections file...")

    myProj = Projections("myProjections.csv",main.hitters,mainPitchers.pitchers)
    myProj.writeRows()

    print("Projections written to ", myProj.file)
                
def personalTouch(guys):
    ''' This is where I change some guys stats because Steamer is wrong. Like Joey Votto is not a .283 hitter.'''

    for guy in guys:
        if guy.playerID == "playerIDIDMN":
            ###peronal touch here....
            pass

def Defensive(file):
    '''add a fangraphs file of last year's defensive stats, for getting players innings at each position.'''
    players = []
    with open(file, 'r',newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(data)
        for line in data:##stats are name, playerID, POS, Inn
            
            temp = Defender(line[0],line[25],line[2],line[3])
            players.append(temp)
    return players

        
def averageIP(guy1,guy2):
    return guy1.IP*.5 + guy2.IP*.5

def averageSV(guy1,guy2):
    IP = guy1.IP
    guy2.adjToIP(IP)
    out = guy2.SV
                    
        
def averageRBI(guy1,guy2):
    ##print(guy1.RBI, type(guy1.RBI))
    RBI1 = guy1.RBI - guy1.HR
    RBI2 = guy2.RBI - guy2.HR
    return (RBI1 + RBI2)/2 + guy1.HR

def averageR(guy1, guy2):
    R1 = guy1.R - guy1.HR
    R2 = guy2.R - guy2.HR
    return (R1 + R2)/2 + guy1.HR
                

    

class Projections:

    def __init__(self,file,hitters,pitchers):
        self.header = ["Name", "Pos","PA/IP", "BA","R","HR","RBI","SB","ERA","WHIP","W","SO","SV","fWAR"]
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
        out = [hitter.name,temp,hitter.PA,hitter.BA(),hitter.R,hitter.HR,hitter.RBI,hitter.SB,'','','','','',hitter.fWAR()]
        return out

    def pitcherData(self,pitcher):
        out = [pitcher.name,"P",pitcher.IP,'','','','','',pitcher.ERA(),pitcher.WHIP(),pitcher.W,pitcher.SO,pitcher.SV,pitcher.fWAR()]
        return out

    
class FansHitters():

    def __init__(self,file):
        self.file = file
        self.hitters = []
        file = open(file,'r')
        file = csv.reader(file, delimiter =',', quotechar= '"')
        self.header = next(file)
        self.header[0] = 'Name'

##        for n in range(len(self.header)):
##            print(n, self.header[n])

        for player in file:
            ##print(player)
            temp = self.createHitter(player)
            self.hitters.append(temp)

            
                   

    def createHitter(self, guy):
        '''return a hitter object from the text of a row.'''
        out = Hitter(guy[0],
                     int(guy[2]),
                     int(guy[3]),
                     int(guy[4]),
                     int(guy[11]),
                     int(guy[5]),
                     int(guy[6]),
                     int(guy[7]),
                     int(guy[8]),
                     int(guy[9]),
                     int(guy[10]),
                     int(guy[14]),
                     int(guy[15]),
                     int(guy[12]),
                     guy[24]
                     )
        ##out.printPlayer()
            
        out.H1B = out.H1B - out.H2B - out.H3B - out.HR
        out.hits = out.calcHits()
        ##print(out.hits())
        return out

        

class HitterFile():
    '''For handling files of baseball hitters. Inheritance can handle different common
fill types. Will use the hitter class to generate outputs.'''
    
    def __init__(self, file):
        self.file = file
        self.hitters = []
        file = open(file,'r')
        file = csv.reader(file, delimiter =',', quotechar= '"')
        self.header = next(file)
        self.header[0] = 'Name'
        ##print(self.header)

##        for n in range(len(self.header)):
##            print(n, self.header[n])

        for player in file:
            ##print(player)
            temp = self.createHitter(player)
            self.hitters.append(temp)

            
                   

    def createHitter(self, guy):
        '''return a hitter object from the text of a row.'''
        out = Hitter(guy[0],
                     0,
                     int(guy[2]),
                     int(guy[3]),
                     int(guy[10]),
                     int(guy[4]),
                     int(guy[5]),
                     int(guy[6]),
                     int(guy[7]),
                     int(guy[8]),
                     int(guy[9]),
                     int(guy[13]),
                     int(guy[14]),
                     int(guy[11]),
                     guy[29]
                     )
        ##out.printPlayer()
            
        out.H1B = out.H1B - out.H2B - out.H3B - out.HR
        ##out.hits = out.H1B + out.H2B + out.H3B + out.HR
        out.hits = out.calcHits()
        ##print(out.hits())
        return out
        

    


class Hitter:

    spgxH = 9.20
    spgHR = 3.75
    spgR = 11.32
    spgRBI = 8.48
    spgSB = 4.49
    lgBA = .270
    replacementLevel = 16.87
    
    def __init__(self, name, G, PA, AB, BB, H1B, H2B, H3B, HR, R, RBI, SB, CS, SO, playerID):
        try: ##verify the data is proper type:
            (G + PA + AB + H1B + H2B +H3B + HR + R + RBI + SB + CS + SO)
        except:
            print("This object was created with non integer types for numerical variables.")
            
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
            '1B' : False,
            '2B' : False,
            '3B' : False,
            'SS' : False,
            'C'  : False,
            'RF' : False,
            'CF' : False,
            'LF' : False,
            'DH' : False
            }

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
        
        
        
    def calcHits(self):
##        print("What the shit?")
##        print(self.H1B)
##        print(self.HR)
##        print(self.H2B)
##        print(self.H3B)
        output = self.H1B + self.H2B + self.H3B + self.HR
        return output


        

    def TB(self):
        return self.H1B + 2*self.H2B + 3*self.H3B + 4*self.HR

    def SLG(self):
        return self.TB()/self.AB

    def BA(self):
        return self.hits/self.AB

    def OBP(self):
        return (self.hits + self.BB)/(self.AB + self.BB)
    
    def calcxH(self):
        self.xH = (self.BA()-self.lgBA)*self.AB
        return self.xH
        
    def fWAR(self):
        fWAR = self.HR/self.spgHR + self.RBI/self.spgRBI + self.R/self.spgR + self.SB/self.spgSB
        self.xH = self.calcxH()
        fWAR = fWAR + self.xH/self.spgxH - self.replacementLevel
        if self.elig['C']:
            fWAR = fWAR + 2.95
        ##print(fWAR)
        return(round(fWAR,2))

    def addElig(self, pos):
        self.elig[pos]=True


        

class Defender:##very simple, play time only.
    def __init__(self, name, ID, Pos, Inn):
        ##stats are name, playerID, POS, Inn
        self.playerID = ID
        self.name = name
        self.pos = Pos
        self.Inn = Inn

    
        


class Pitcher:
    spgxER = 7.85
    spgSO = 12.99
    spgW = 1.59
    spgSV = 5.19
    spgxWHIP = 10.60
    lgERA = 3.5
    lgWHIP = 1.21
    replacementLevel = 11.44

    def __init__(self,name,W,L,GS,G,SV,IP,H,ER,HR,SO,BB,playerID):
        self.W = W
        self.L = L
        self.GS = GS 
        self.G = G 
        self.SV = SV 
        self.IP = IP 
        self.H = H 
        self.ER = ER
        self.HR = HR
        self.SO = SO
        self.BB = BB
        self.name = name
        self.playerID = playerID


    def ERA(self):
        return self.ER/self.IP*9

    def WHIP(self):
        return (self.BB + self.H)/self.IP

    def xER(self):
        return (self.lgERA - self.ERA())/9 * self.IP

    def xWHIP(self):
        return (self.lgWHIP - self.WHIP())*self.IP

    def adjToIP(self,IP):
        self.formerIP = self.IP
        ratio = IP/self.IP
        self.W = self.W * ratio
        self.L = self.L * ratio
        self.GS = self.GS * ratio
        self.G = self.G  * ratio
        self.SV = self.SV  * ratio
        self.IP = self.IP  * ratio
        self.H = self.H * ratio
        self.ER = self.ER * ratio
        self.HR = self.HR * ratio
        self.SO = self.SO * ratio
        self.BB = self.BB * ratio

    def K_9(self):
        return self.SO/self.IP*9

    def BB_9(self):
        return self.BB/self.IP*9

    def fWAR(self):
        fWAR = self.xER()/self.spgxER + self.xWHIP()/self.spgxWHIP + self.SO/self.spgSO + self.W/self.spgW + self.SV/self.spgSV
        fWAR = fWAR - self.replacementLevel
        return round(fWAR, 2)
        


class FanPitcherFile:

        def __init__(self, file):
            self.file = file
            self.pitchers = []
            file = open(file,'r')
            file = csv.reader(file, delimiter =',', quotechar= '"')
            self.header = next(file)
            self.header[0] = 'Name'

            for player in file:
                ##print(player)
                temp = self.createPitcher(player)
                self.pitchers.append(temp)

        def createPitcher(self,guy):
            output = Pitcher(
                guy[0],
                int(guy[2]),
                int(guy[3]),
                int(guy[5]),
                int(guy[6]),
                int(guy[7]),
                float(guy[8]),
                int(guy[9]),
                int(guy[10]),
                int(guy[11]),
                int(guy[12]),
                int(guy[13]),
                guy[20]
                )
            return output
            

class SteamerPitcherFile(FanPitcherFile):
    '''In 2016, steamer pitcher projections were the same format as fan projections.'''

##        def __init__(self, file):
##            self.file = file
##            self.pitchers = []
##            file = open(file,'r')
##            file = csv.reader(file, delimiter =',', quotechar= '"')
##            self.header = next(file)
##            self.header[0] = 'Name'
##            print(self.header)
##
##            for n in range(len(self.header)):
##                print(n, self.header[n])
##
##            for player in file:
##                ##print(player)
##                temp = self.createPitcher(player)
##                self.pitchers.append(temp)
##
##        def createPitcher(self):
##            pass

    def Dummy(self):
        ##To make this "inherited class distinct.
        pass
        



test()
main()
