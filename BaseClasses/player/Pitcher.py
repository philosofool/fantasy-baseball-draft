from copy import deepcopy
from .Player import Player

class Pitcher(Player):
    spgxER = 8.47# was in 2018, 7.85
    spgSO = 17.47
    spgW = 1.73
    spgSV = 4.55
    spgxWHIP = 12.420
        ###was 10.60 in 2018
        ##Shit, used 10.848 in 2019; actual value in 2019 was 13.992!
    lgERA = 3.79
    lgWHIP = 1.23
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
        self.playerID =playerID

        self.elig = {
            "P" : True
            }
        self.avail = True
        
    def __str__(self):
        return "Pitcher {}".format(self.name)
    
    def __repr__(self):
        return "Pitcher {}".format(self.name)


    def isReliever(self):
        '''
        Return true if a pure reliever
        '''
        if self.GS == 0 and self.IP > 0:
            return True
        else:
            return False

    def hasSaves(self, saves = 4):
        """
        Returns a bool if a player has a certain number of saves.

        Parameters
        ----------

        saves: int, default = 5
            Returns true if and only if Pitcher.SV >= saves.
        """
        if self.SV >= saves:
            return True
        else:
            return False

    def isaStarter(self):
        """
        Return True if a pure starter
        """
        try:
            if self.GS/self.G >= .9:
                return True
            else:
                return False
        except ZeroDivisionError:
            return False

    
    @staticmethod
    def isaPitcher():
        """
        All players should have an isaPitcher(). Overrides Player.isaPitcher() to return True.
        """
        return True
    



    def ERA(self):
        """
        Returns the pitcher's ERA. If the IP attribute is zero, returns zero.
        """
        try:
            return self.ER/self.IP*9
        except ZeroDivisionError:
            return 0

    def WHIP(self):
        try:
            return (self.BB + self.H)/self.IP
        except ZeroDivisionError:
            return 0

    def xER(self):
        return (self.lgERA - self.ERA())/9 * self.IP

    def xWHIP(self):
        return (self.lgWHIP - self.WHIP())*self.IP

    def adjToIP(self,IP):
        """
        Normalizes all the players counting stats to a new number of IP.

        Parameters
        ----------
        IP : numeric
            The number of IP the player is adjusted to. 
            In order to prevent data loss, zero is not allowed and passing zero will have no effect.
            To approximate zero, pass a small float (.01) as PA.

            If the player's IP are already Zero, this has no effect
        """

        try:
            if IP == 0:
                pass
            else:
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
        except ZeroDivisionError:
            print("Pitcher {} has 0 IP. Cannot adjust stats to innings pitched.".format(self))

        
    def asNumberIP(self,ip):
        guy = deepcopy(self)
        guy.adjToIP(ip)
        return guy


    def K_9(self):
        return self.SO/self.IP*9

    def BB_9(self):
        return self.BB/self.IP*9

    def fWAR(self):
        fWAR = self.xER()/self.spgxER + self.xWHIP()/self.spgxWHIP + self.SO/self.spgSO + self.W/self.spgW + self.SV/self.spgSV
        fWAR = fWAR - self.replacementLevel
        return fWAR
    
    def fWARc(self):
        '''I don't love the name here, 'c' is closer. This is fWAR not counting saves, which gives a sense
        of how valuable his non-save performance is.'''
        fWAR = self.xER()/self.spgxER + self.xWHIP()/self.spgxWHIP + self.SO/self.spgSO + self.W/self.spgW# + self.SV/self.spgSV
        fWAR = fWAR - self.replacementLevel
        return fWAR

    def rawWAR(self):
        fWAR = self.xER()/self.spgxER + self.xWHIP()/self.spgxWHIP + self.SO/self.spgSO + self.W/self.spgW + self.SV/self.spgSV
        ##fWAR = fWAR - self.replacementLevel
        return fWAR


    def fWAR150(self):
        '''Returns fWAR150 for starters, or it returns fWAR(). 
        I'm not sure about that. The idea is obviously that relievers should je be thought of as
        giving all their innings and this allows relievers to be compared with each other that way.'''
        IP = self.IP
        if self.isaStarter():
            self.adjToIP(150)
            fWAR150 = self.rawWAR()
            self.adjToIP(IP)
            return fWAR150
        else:
            self.adjToIP(65)
            fWAR150 = self.rawWAR()
            self.adjToIP(IP)
            return fWAR150
        
    def assistLine(self):
        guy = self
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        
        basic = '{0:20} {1:10} {4:11} {2:6.2f} {3:5.2f} '.format(guy.name[0:17],team, guy.fWAR(), guy.fWAR150(), guy.printElig())
        full = '   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:3.0f}  W {4:2.0f}  SV {5:2.0f}  ADP {6:6}'.format(guy.IP, guy.ERA(), guy.WHIP(), guy.SO,  guy.W, guy.SV, guy.ADP)
        return (basic + full)
    
    def spgLine(self):
        guy = self##dumb artifact, but I don't want to fix the typing.
        team = guy.team
        if team == "Diamondbacks":
            team = "Dbacks"
        ##self.xER()/self.spgxER + self.xWHIP()/self.spgxWHIP + self.SO/self.spgSO + self.W/self.spgW + self.SV/self.spgSV##
        basic = '{0:20} {1:10} {4:11} {2:6.2f} {3:5.2f} '.format(guy.name[0:17],team, guy.fWAR(), guy.fWAR150(), guy.printElig())
        full = '   IP {0:3.0f}  ERA {1:5.2f}  WHIP {2:4.2f}  K {3:4.2f}  W {4:4.2f}  SV {5:4.2f}  ADP {6:6}'.format(guy.IP, self.xER()/self.spgxER, self.xWHIP()/self.spgxWHIP, self.SO/self.spgSO,  self.W/self.spgW, self.SV/self.spgSV, guy.ADP)
        return (basic + full)
        
