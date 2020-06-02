'''
Takes a standard output from fangraphs and turns them in KLF valuations.

'''

def main():
    project("Fans/catcher.csv","Projections/catchers.csv")
    project("Fans/firstbase.csv","Projections/firstbase.csv")
    project("Fans/secondbase.csv","Projections/secondbase.csv")
    project("Fans/thirdbase.csv","Projections/thirdbase.csv")
    project("Fans/shortstop.csv","Projections/shortstop.csv")
    project("Fans/rightfield.csv","Projections/rightfield.csv")
    project("Fans/centerfield.csv","Projections/centerfield.csv")
    project("Fans/leftfield.csv","Projections/leftfield.csv")
    project("Fans/outfield.csv","Projections/outfield.csv")
    project("Fans/designatedhitter.csv","Projections/designatedhitter.csv")
    positions = ["C","1B","2B","3B","SS","RF","CF","LF","OF","DH"]
    sheets = ["Projections/catchers.csv",
    "Projections/firstbase.csv",
    "Projections/secondbase.csv",
    "Projections/thirdbase.csv",
    "Projections/shortstop.csv",
    "Projections/rightfield.csv",
    "Projections/centerfield.csv",
    "Projections/leftfield.csv",
    "Projections/outfield.csv",
    "Projections/designatedhitter.csv"]
    master = open("Projections/all_hitters.csv",'w')
    master.write("Position,Player,PA,AB,R,BA,HR,RBI,SB,fWAR,BRAA/600\n")
    n = 0
    for sheet in sheets:
        file = open(sheet,'r')
        file.readline()
        for line in file.readlines():
            master.write(positions[n] + ",")
            master.write(line)
        file.close()
        n = n + 1
    master.close()
    redundant = open("Projections/all_hitters.csv",'r')
    master = open("Projections/new_hitters.csv",'w')
    redundant_list = []
    master_set = set()
    for line in redundant.readlines():
        #print(line)
        if line.split(",")[1] in master_set:
            pass
        else:
            #print(line)
            master_set.add(line.split(",")[1])
            master.write(line)
    master.close()
                           

def project(infile,outfile):
    ZiPS = leaders("ZiPS Leaders 2014.csv")
    fans = leaders(infile)
    aggregate = []

    projections = open(outfile,'w')
    
    for player in fans:
        for projected in ZiPS:
            if projected.id == player.id:
                projected.adjToPA(player.PA)
                projected.RBI = (player.RBI + projected.RBI - player.HR - projected.HR)/2 + projected.HR
                projected.runs = (player.runs + projected.runs - player.HR - projected.HR)/2 + projected.HR
                aggregate.append(projected)
                break

    projections.write("Player,PA,AB,R,BA,HR,RBI,SB,fWAR,BRAA/600\n")
    for player in aggregate:
        projections.write((player.line())+"\n")

    projections.close()

def leaders(leaderboard):
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
    print(file)
    file.readline()
    for line in file.readlines():
        a = line.replace('"','')
        #hitter = Hitter(a)
        players.append(Hitter(cleanUp(a)))
    return players

def cleanUp(line):
    #print(line)
    b = []
    a = line.split(",")
    b.append(a[0])
    for number in a[1:15]:
        b.append(int(number))
    for number in a[15:20]:
        b.append(float(number))
    try:
        b.append(float(a[20]))
    except: print(a)
    b.append(float(a[21]))
    b.append(float(a[22]))
    try:
        b.append(int(a[23]))
    except:
        b.append(a[23])
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
        self.evaluate()
        out = self.name + ","
        out = out + statForm(self.PA) +","
        out = out + statForm(self.AB) + ","
        out = out + statForm(self.runs) + ","
        out = out + format(self.hits/self.AB,'.3f') + ","
        out = out + statForm(self.HR) + ","
        out = out + statForm(self.RBI) + ","
        out = out + statForm(self.SB) + ","
        out = out + statForm(self.fWAR) + ","
        out = out + statForm(self.fBRAA/self.PA*600)
        return out

    def evaluate(self):
        # some spg constants
        spgHR = 5.1
        spgR = 11.8
        spgRBI = 12.5
        spgxH = 9.53
        spgSB = 4.8
        avAVG = .270
        repLevel = 15.0
        fBRAA = self.HR/spgHR + self.RBI/spgRBI + self.runs/spgR + self.SB/spgSB
        xH = ((self.hits/self.AB) - avAVG) * self.AB
        fBRAA = fBRAA + xH/spgxH
        self.fWAR = fBRAA - repLevel
        self.fBRAA = fBRAA
        #return fBRAA

def statForm(stat):
    return format(stat, '.1f')
    

main()
