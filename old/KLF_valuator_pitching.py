'''
Takes a standard output from fangraphs and turns them in KLF valuations.

'''

def main():


    ZiPS = leaders("ZiPS_pitchers.csv")
    #ZiPS pitching files do not include saves. Add a column for saves!!! It should be
    #after G and before IP, and be full of 0's
    fans = leaders("Fans_pitchers.csv")
    aggregate = []

    projections = open('Projections/pitchers.csv','w')

    for player in fans:

        for projected in ZiPS:
            if projected.id == player.id:
                projected.adjToIP(player.IP)
                projected.saves = player.saves
                projected.evaluate()
                aggregate.append(projected)
                break

    #print(aggregate)
    projections.write("Name,Role,IP,W,S,ERA,WHIP,SO, fWAR, fPRAA\n")
    for player in aggregate:
        projections.write((player.line())+"\n")

    projections.close()
    

def leaders(leaderboard):
    '''
    returns list a of lists b, where b lists are lists of player names and stats.
    '''
    leaders = open(leaderboard,'r')
    
    leaders = fanFileToList(leaders)
    #playersValued = evaluate(players)
    leaders.pop()
    return leaders

#then just write all the players to a file.

def fanFileToList(file):
    '''Creates a list of lists. Each item in the primary list is a list of the
    stats in a fangraphs file line, with numerals turned to numbers.'''
    players= []
    file.readline()
    for line in file.readlines():
        a = line.replace('"','')
        #hitter = Hitter(a)
        players.append(Pitcher(cleanUp(a)))
    return players

def cleanUp(line):
    '''
    Returns a line from a stat file as a list, with numbers in place of strings
       as appropriate.
    '''
    b = []
    a = line.split(",")
    b.append(a[0])
    for number in a[1:13]:
        try:
            b.append(int(number))
        except:
            b.append(float(number))
    for number in a[13:18]:
        b.append(float(number))
    #b.append(int(a[20]))
    #b.append(float(a[21]))
    #b.append(float(a[22]))
    try:
        b.append(int(a[18]))
    except:
        b.append(a[18].strip("\n"))
    #print(b)
    return b

##def evaluate(players):
##    spgHR = 5.1
##    spgR = 11.8
##    spgRBI = 12.5
##    spgxH = 9.53
##    spgSB = 4.8
##    avAVG = .270
##    for player in players:
##        player.value = player.HR()/spgHR
##        player.value = player.value + player.RBI()/spgRBI + player.R()/spgR + player.SB()/spgSB
##        player.xH = player.AB()*(player.AVG() - avAVG)
##        player.value = player.value + player.xH/spgxH
##        print(player.value)
##
##    return "What the hell did you return?"

class Pitcher:
    def __init__(self,line):
        self.id = line[18]
        self.IP = line[7]
        self.hits = line[8]
        self.BB = line[12]
        self.ER = line[9]
        self.wins = line[1]
        self.saves = line[6]
        self.name = line[0]
        self.K = line[11]
        self.G = int(line[5])
        self.GS = int(line[4])

    def adjToIP(self, IP):
        ratio = IP/self.IP
        self.IP = IP
        self.hits = self.hits * ratio
        self.BB = self.BB * ratio
        self.ER = self.ER * ratio
        self.wins = self.wins * ratio
        self.saves = self.saves * ratio
        self.K = self.K * ratio

    def ERA(self):
        return self.ER/self.IP*9

    def WHIP(self):
        whip = (self.hits + self.BB)/self.IP
        return whip
    def line(self):
        if self.role == "RP":
            roleIP = 60
        else:
            roleIP = 160
        out = self.name + ","
        out = out + self.role() + ","
        out = out + statForm(self.IP) +","
        out = out + statForm(self.wins) + ","
        out =  out + statForm(self.saves) + ","
        out = out + statForm(self.ERA()) + ","
        out = out + statForm(self.WHIP()) + ","
        #out = out + statForm(self.BB) + ","
        out = out + statForm(self.K) + ","
        out = out +statForm(self.fWAR) + ","
        out = out + statForm(self.fPRAA/self.IP*roleIP)
        return out

    def role(self):
        if self.GS > .8 * self.G:
            return "SP"
        elif self.GS < .2 * self.G:
            return "RP"
        else:
            return "Swing"

    def evaluate(self):
        '''produces a fantasy value above replacement as an attribute'''
        # Some SPG constants
        xERspg = 7.45
        xWHIPspg = 13.43
        SOspg = 18.1
        savesspg = 5.6
        winsspg = 2.9
        avERA = 3.69
        avWHIP = 1.25
        repLevel = 9.7

        xER = (avERA - self.ERA())/9*self.IP
        xWHIP = (avWHIP - self.WHIP())*self.IP

        fPRAA = self.K/SOspg + self.wins/winsspg + self.saves/savesspg + xER/xERspg + xWHIP/xWHIPspg

        self.fWAR = (fPRAA - repLevel)*.8
        self.fPRAA = fPRAA*.8

class Hitter:
    def __init__(self, line):
        self.id = line[23]
        self.hits = line[4]
        self.RBI = line[9]
        self.runs = line[8]
        self.HR = line[7]
        self.AB = line[3]
        self.PA = line[2]
        self.SB = line[13]
        self.name = line[0]

    def adjToPA(self, PA):
        
        ratio = PA/self.PA
        self.PA = PA
        self.hits = self.hits * ratio
        self.HR = self.HR * ratio
        self.RBI = self.RBI * ratio
        self.runs = self.runs * ratio
        self.SB = self.SB * ratio
        self.AB = self.AB * ratio

    def line(self):
        out = self.name + ","
        out = out + statForm(self.PA) +","
        out = out + statForm(self.AB) + ","
        out = out + statForm(self.runs) + ","
        out = out + statForm(self.hits) + ","
        out = out + statForm(self.HR) + ","
        out = out + statForm(self.RBI) + ","
        out = out + statForm(self.SB)
        return out

def statForm(stat):
    return format(stat, '.2f')
    

main()
