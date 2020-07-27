import csv

from BaseClasses.player.Hitter import Hitter
from BaseClasses.player.Pitcher import Pitcher
from BaseClasses.team.Team import Team
        
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
    '''
    basically just writes results to a file. 
    Results? Results of what? Jesus.
    '''
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

    
class FansHitters(list):

    def __init__(self,file):
        self.file = file
        ##self.hitters = []
        file = open(file,'r')
        file = csv.reader(file, delimiter =',', quotechar= '"')
        self.header = next(file)
        self.header[0] = 'Name'

##        for n in range(len(self.header)):
##            print(n, self.header[n])

        for player in file:
            ##print(player)
            temp = self.createHitter(player)
            self.append(temp)

            
                   

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

        

class HitterFile(list):
    '''For handling files of baseball hitters. Inheritance can handle different common
fill types. Will use the hitter class to generate outputs.'''

    leagueHitterDepth = 180
    
    def __init__(self, file):
        self.file = file
        #self.players = []
        file = open(file,'r')
        file = csv.DictReader(file, delimiter =',', quotechar= '"')
        self.file = file
        #print(file.fieldnames)
        if self.file.fieldnames[0] != 'Name':
            self.file.fieldnames[0] = 'Name'
        for player in file:
            temp = self.createHitter(player)
            self.append(temp)
                               

    def createHitter(self, guy):
        '''return a hitter object from the text of a row.'''
        #print("Guy is ....\n",guy)
        try:
            out = Hitter(guy['Name'],##names
                         int(guy['G']),##games
                         int(guy['PA']),##pa
                         int(guy['AB']),##ab
                         int(guy['BB']),##BB
                         int(guy['H']),##hits, usually; you need to double check whether this is hits or singles. It's singles in the hitter object.
                         int(guy['2B']),##doubles
                         int(guy['3B']),##triples
                         int(guy['HR']),##HR
                         int(guy['R']),##R
                         int(guy['RBI']),##RBI
                         int(guy['SB']),##SB
                         int(guy['CS']),##CS
                         int(guy['SO']),##SO
                         guy['playerid']##player ID
                         )
            try:
                out.ADP = guy['ADP']
            except:
                out.APD = 1000
                
            out.H1B = out.H1B - out.H2B - out.H3B - out.HR
            out.hits = out.calcHits()
            out.team = guy['Team']##his team in MLB
            ##print(out.hits())
            return out
        except KeyError:
            print("{}.createHitter() encountered a key error with {}".format(self,guy))
            raise Exception
            #raise KeyError


    def replacementLevel(self,rank = leagueHitterDepth):## 
        temp = [] + self
        temp.sort(key = lambda player: player.rawWAR(), reverse = True)
        return temp[rank].rawWAR()
    
class CBSHitters(HitterFile):
    def __init__(self, file):
        self.PID = 0#player id number
        self.file = file
        #self.players = []
        file = open(file,'r')
        file = csv.DictReader(file, delimiter =',', quotechar= '"')
        self.file = file
        print(file.fieldnames)
        #if self.file.fieldnames[0] != 'Name':
        #    self.file.fieldnames[0] = 'Name'
        for player in file:
            temp = self.createHitter(player)
            self.append(temp)
        file.close()

    def createHitter(self, guy):
        '''return a hitter object from the text of a row.'''
        #print("Guy is ....\n",guy)
        try:
            hits = int(rouind(int(guy['AB']) * float(guy['AVG'])))
            CS = -1
            out = Hitter(guy['Player'],##names
                         int(guy['G']),##games
                         int(guy['BPA']),##pa
                         int(guy['AB']),##ab
                         int(guy['BB']),##BB
                         int(hits),##hits, usually; you need to double check whether this is hits or singles. It's singles in the hitter object.
                         int(guy['2B']),##doubles
                         int(guy['3B']),##triples
                         int(guy['HR']),##HR
                         int(guy['R']),##R
                         int(guy['RBI']),##RBI
                         int(guy['SB']),##SB
                         int(CS),##CS; not defined. -1 will remindme of that.
                         int(guy['K']),##SO
                         self.PID##player ID
                         )
            try:
                out.ADP = guy['ADP']
            except:
                out.APD = 1000
                
            elig = guy['Eligible'].split()
            for pos in elig:
                guy.addElig(pos)
                
            out.H1B = out.H1B - out.H2B - out.H3B - out.HR
            out.hits = out.calcHits()
            try:
                out.team = guy['Team']##his team in MLB
            except:
                out.team = None
            ##print(out.hits())
            self.PID += 1
            return out
        
        except KeyError:
            print("{}.createHitter() encountered a key error with {}".format(self,guy))
            raise Exception
            #raise KeyError

    
class ClosersFile:
    '''This is a pretty specific file format for fantasy purposes.
    It is a list of team and data about their bullpen sitch. Not the easiest thing
    to work with from this end, but that's the way they list them on websides
    most of the time, and the assholes don't make the sheet of closers downloadable.
    File format is Tema, Division, Closer, Security,fWARc,Handcuff1,Handcuff2,Handcuff3,Handcuff4
    '''
    def __init__(self,file):
       file = open(file,'r')
       file = csv.DictReader(file, delimiter=',',quotechar='"')
       self.file = file
       self.file.fieldnames[0] = 'Team'
       self.teams = []
       for line in file:
           team = CloserTeam(line['Team'],line['Closer'],line['Security'])
           for e in self.file.fieldnames[-4:]:
               if line[e]:
                   team.handcuffs.append(line[e])
           self.teams.append(team)
       
           
       
        
    def guysAsPitchers(self,pitchers):
        '''This takes a list of pitcher objects and replaces the guys in the team with pitcher objects.
        '''
        for team in self.teams:
            for guy in pitchers:
                if guy.name == team.closer:
                    team.closer = guy
                elif guy.name in team.handcuffs:
                    team.handcuffs.append(guy)
                    team.handcuffs.remove(guy.name)
                    
    def listNonPitchers(self,verbose=False):
        '''This lists all players in the file who are not stored as pitcher objects, use after "guysAsPitchers" to verify'''
        out = ""
        if verbose:
            print("Printing list of pitchers in teams that are not stored as an instance of class Pitcher.")
        for team in self.teams:
            try:
                team.closer.isaPitcher()
                if verbose:
                    print("{} is recorded as pitcher object.".format(team.closer.name))
            except:
                out += "{} {}\n".format(team.team,team.closer)
            for guy in team.handcuffs:
                try:
                    guy.isaPitcher()
                    if verbose:
                        print("{} is recorded as pitcher object.".format(guy.name))                        
                except:
                    out += "{} {}\n".format(team.team,guy)
        return out
    
    def listClosers(self):
        '''creates a list output of all the closers in the list'''
        allGuys = []
        for team in self.file:
            try:
                team.closer.isaPitcher()
                allGuys.append(team.closer)
            except:
                pass
            for guy in team.handcuffs:
                try:
                    guy.isaPitcher()
                    allGuys.append(guy)
                except:
                    pass
        return allGuys
    
    def closersWithStrength(self,strength):
        guys = []
        for team in self.teams:
            if team.strength.lower() == strength.lower():
                guys.append(team.closer)
        return guys
    
    def teamsWithStrength(self,strength):
        out = []
        for team in self.teams:
            if team.strength.lower() == strength.lower():
                out.append(team)
        return out
        
class CloserTeam:
    def __init__(self,team,closer,strength):
        self.name = team
        self.strength = strength##positional security of the closer
        self.closer = closer
        self.handcuffs = []
        
    def guyIsOn(self,guy):
        '''returns true if a guy is found on the team, false otherwise.'''
        if guy == self.closer or guy in self.handcuffs:
            return True
        else:
            return False
        
    

class FanPitcherFile(list):

    def __init__(self, file):
        self.file = file
        #self.players = []
        file = open(file,'r')
        file = csv.DictReader(file, delimiter =',', quotechar= '"')
        self.file = file
        #print(file.fieldnames)
        if self.file.fieldnames[0] != 'Name':
            self.file.fieldnames[0] = 'Name'
#        self.file = file
#        file = open(file,'r')
#        file = csv.reader(file, delimiter =',', quotechar= '"')
#        self.header = next(file)
#        self.header[0] = 'Name'

        for player in file:
            ##print(player)
            temp = self.createPitcher(player)
            self.append(temp)
        #file.close()

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
            

class DepthPitcherFile(FanPitcherFile):
    '''For fangraphs depth projections.'''

    leaguePitcherDepth = 165
    def createPitcher(self,guy):
        output = Pitcher(##pitcher object gets name,W,L,GS,G,SV,IP,H,ER,HR,SO,BB,playerID
            guy['Name'],##name
            int(guy['W']),##W
            int(guy["L"]),##L
            int(guy['GS']),##GS
            int(guy['G']),##G
            int(guy['SV']),##SV
            float(guy['IP']),##IP
            int(guy['H']),##H
            int(guy['ER']),##ER
            int(guy['HR']),##HR
            int(guy['SO']),##SO
            int(guy['BB']),##BB
            guy['playerid']##player ID
            )
        output.team = guy['Team']
        try:
            output.ADP = guy['ADP']
        except:
            output.ADP = 1001
        
        return output

    def replacementLevel(self,rank = leaguePitcherDepth):
        temp = [] + self
        temp.sort(key = lambda player: player.rawWAR(), reverse = True)
        return temp[rank].rawWAR()
        

class CBSHitterProjections(HitterFile):
    def __init__(self, file):
        self.file = file
        #self.players = []
        file = open(file,'r')
        file.readline()
        header = file.readline()
        header = header.split(",")
        file = csv.DictReader(file, delimiter =',', quotechar= '"',fieldnames=header)
        self.file = file
        #print(file.fieldnames)
#        if self.file.fieldnames[0] != 'Name':
#            self.file.fieldnames[0] = 'Name'
        self.playerid = 0
        for player in file:
            temp = self.createHitter(player)
            if type(temp) == Hitter:
                   self.append(temp)
        

    def createHitter(self, guy):
        '''return a hitter object from the text of a row.'''
        #print("Guy is ....\n",guy)
        name = CBSFilePlayers.extractName(self,guy['Player'])
        #print(guy.keys())
        try:
            out = Hitter(name,##names
                         int(guy['G']),##games
                         int(guy['BPA']),##pa
                         int(guy['AB']),##ab
                         int(guy['BB']),##BB
                         int(guy['1B']),##hits, usually; you need to double check whether this is hits or singles. It's singles in the hitter object.
                         int(guy['2B']),##doubles
                         int(guy['3B']),##triples
                         int(guy['HR']),##HR
                         int(guy['R']),##R
                         int(guy['RBI']),##RBI
                         int(guy['SB']),##SB
                         int(guy['CS']),##CS
                         int(guy['K']),##SO
                         self.playerID()##player ID
                         )
                
            #out.H1B = out.H1B - out.H2B - out.H3B - out.HR
            out.hits = out.calcHits()
            #out.team = guy['Team']##his team in MLB
            ##print(out.hits())
            return out
        except KeyError:
            print("{}.createHitter() encountered a key error with {}".format(self,guy))
            raise Exception
            #raise KeyError
        except ValueError:
            print("Exception raised by in CBSHitterProjections in createHitter with {}. Skipping his ass.".format(guy['Player']))
        
    def playerID(self):
        '''generates a player id for the sake of giving one.'''
        out = self.playerid
        self.playerid += 1
        return out
    

class CBSFilePlayers(list):
    '''Just a list of players and eligibities, etc. '''
    def __init__(self,file):
        file = open(file,'r')
        file = csv.DictReader(file,delimiter=',', fieldnames = ["Avail","Player","Eligible"],quotechar='"')
        next(file)
        next(file)
        for player in file:
            try:
                name = self.extractName(player['Player'])
                if name == "Seung-Hwan Oh":
                    name = "Seung Hwan Oh"
                if name == "Vladimir Guerrero":
                    pass#you have a new, better solution
                    #name = "Vladimir Guerrero Jr."
                    #print( player's name to {}".format(name))
                avail = player['Avail']
                pos = player['Eligible']
                pos = pos.split(",")
                self.append(SimplePlayer(name,avail,pos))
            except:
                ##print("Exception called for {}".format(player))
                pass
        self.repeatedPlayerNames = []
        self.repeatedNames()

    def names(self):
        out = []
        for guy in self:
            out.append(guy.name)
        return out
    
    def sortByName(self):
        self.sort(key = lambda guy: guy.name, reverse = True)

    def getIfOnTeam(self,team):
        print("Depricated method 'getIfOnTeam' called by CBSPlayer Object. use list of guys on team instead.")
        out = []
        for guy in self:
            if team.lower() in guy.avail.lower():
                out.append(guy)
        return out

    def listOfGuysOnTeam(self,team):
        out = []
        for guy in self:
            if team.lower()[:3] in guy.avail.lower()[:3]:
                out.append(guy)
        return out
    
    def listOfFreeAgents(self):
        out = []
        for guy in self:
            if guy.avail[:2] == "FA" or guy.avail[:3] == "W (":
                out.append(guy)
                
        return out


    def extractName(self, entry, verbose = False):
        try:
            b = entry.split()
        ##        name = b[0] + " " + b[1]
        ##        print(name)
            if len(b) > 6:
                name = " ".join(b[0:4])
                return name
            elif len(b) >= 6:
                name = " ".join(b[0:3])
                return name
            else:
                name = " ".join(b[0:2])
                return name
        except:
            if verbose:
                print("Could not extract name from {}".format(entry))

    def repeatedNames(self):
        '''a list of all names in the file that are repeated, i.e., belong to more than one guy.'''
        out = []
        temp = []
        for guy in self:
            if guy.name in temp:
                out.append(guy.name)
                self.repeatedPlayerNames.append(guy.name)##This is a very slow process, so this attribute helps speed stuff up, like "x in self.repeatedPlayerNames"
            else:
                temp.append(guy.name)

        return out


    def playersAtPosition(self,pos):
        '''returns the list of guys whose position matches the filter'''
        out = []
        for guy in self:
            if pos in guy.elig:
                out.append(guy)
        return out

    @staticmethod
    def playerIntersection(guys1,guys2):
        ''' Returns a list of objects found in each of two lists, matched by name.
            Any object with attribute .name will work.
            Returned list contains objects from first argument, guys1.
    '''
        guys1.sort(key = lambda guy: guy.name, reverse = True)
        guys2.sort(key = lambda guy: guy.name, reverse = True)
        out = []
        for guy in guys1:
            for dude in guys2:##start with the alphabetically first guy in guys2
                if guy.name == dude.name:
                    out.append(guy)
                if dude.name < guy.name: ##if guy.name isn't after dude.name, alphaphetically, stop the loop
                    #print(dude.name,guy.name)
                    break

        return out



class SimplePlayer:
    '''Creates a simple player with eligibility, availablity, name, team
       Basically for tracking available CBS players and getting CBS eligibilities.
    '''
    def __str__(self):
        return "Simple Player {}".format(self.name)
        
    def __init__(self, name, avail, elig):
        self.name = name
        self.avail = avail
        self.elig = elig

    def printSelf(self):
        print(self.name, self.avail, self.elig)
        
    

##test()
##closers()
##main()
