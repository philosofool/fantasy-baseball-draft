import csv
from copy import deepcopy
from .Player import Player


class Hitter(Player):
    """Class for representing baseball hitters. Functionality for representing players in a fantasy league is provided.

    ...
    Attributes
    ----------

    In typical boxscore counting stats are represented as attributes and properties. Rate stats are methods. 
    Baseball uses capital letters to abbreviate these things as this follows that convention, hence "player.RBI" rather than "player.rbi"
    To provide funcationality for projection, etc., the values of the counting stats can be integers or floats.

    name : str
        First and last name of player, including any suffic (e.g. 'Jr.') Note that names are not standard across all sources. No convention is used here to determine which source or standard to use. 

    games : numeric
        number of games in which player made an appearance, indluces games in which the player did not appear at the plate, since that's the way box score data works.

    PA : numeric
        Plate apperances.

    BB : numeric
        Number of times the batter walked. Include intentional and unintentional walks.

    H1B : numeric
        Singles. '1B' is the baseball conventional notation but python does not allow attributes beginning with numerals. Hence, all counts of hits are preceded with an 'H' for 'hits.'

    H2B : numeric
        Doubles. (See singles for more information about conventions.)

    H3B : numeric
        Triples (See singles for more information about conventions.)

    HR : numeric
        Home runs hit. 

    R : numeric
        Runs scored.

    RBI : numeric
        Runs batted in.

    SB : numeric
        Stolen bases.

    CS : numeric
        Caught stealing.

    SO : numeric
        Strike outs.

    playerID : string
        a field for a unique player identifier, such as from a database.
        This value is not expected to change and should function with non-string (e.g., int) types but string is preferred.

    hits : numeric
        total number of hits. Equals H1B + H2B + H3B + HR.

    elig : dict
        Eligibility. A dictionary with keys 'C', '1B', '2B', '3B' etc. with values set to true or false, based on whether the player is eligible at the relevant position.

    avail : string
        Avaliablity. A string to hold values such as "free agent" describing whether the player is availble in the league.

    team : string
        Name of the player's team.

    Class Attributes
    ----------------

    spgxH : float
        Standings points gained for xH, expected hits above average. 
        xH = (player batting average - league average)*at bats.
    spgHR : float
        Stanging points gained for home runs.
    spgR : float
        Standings points gained for runs.
    spgRBI : float
        Standings points gained for RBIs.
    spgSB : float
        Standings points gained for Stolen bases
    lgBA : float
        The batting average of the league.
    replacementLevel : float
        The fantasy baseball replacement level standings points gained.
    catcherReplacement : float
        The fantasy baseball replacement level standings points gained for catchers, who are generally worse than 
        your typical player.

    Methods
    -------
    In general, methods for generating statndard baseball stats from box score data. All rate stats are methods, 
    as well as some counting stats (e.g., total bases) that are dependent on these. 

    SGL()
        Returns the player's slugging percentage. Returns zero for players with no at bats.
    BA()
        Returns the player's batting average. Returns zero for players with no at bats.
    TB()
        Returns the player's total bases, 4*HR + 3*H3B + 2*H2B + H1B.
    OBP()
        Returns the player's on base percentage. Returns zero for players with no plate appearances. 
    printPlayer()
        Prints player's attributes. Mostly for testing/validation.
    adjToPA(PA)
        Normalizes player's stats to PA number of plate appearances.
    asNumberPA(PA)
        Returns a copy of the player, normalized to a number of plate appearnaces using adjToPA(PA).
    calcHits()
        Returns number of hits (HR + triples + doubles + singles).
    calcxH()
        Returns the number of expected hits above average.
    fWAR()
        Returns the player's fantasy "wins" above replacement player, which is standings points gained above replacement level.
    rawRAW()
        Returns the sum of the player's stangings points gained.
    multiEligible()
        Returns True if the player is eligible at multiple positions. Else, returns False.
    assistLine()
        Returns a string 'box score' style line for the players fantasy relevant stats. 
    addElig(position)
        Sets eligiblity for a position to True.
        




    """

    spgxH = 8.475##used 8.47, nearly matched the real value of 8.486 in 2019.
    spgHR = 5.286##real value was 4.782
    spgR = 11.671###used 10.81,real value was 12.532
    spgRBI = 13.38##used 12.20,was 14.564
    spgSB = 3.46##used 4.27,was 2.657
    lgBA = .265
    replacementLevel = 16.72
    catcherReplacement = 9##This is an approximation. Draft assistant has methods for finding it in a list

    
    def __init__(self, name, G, PA, AB, BB, H1B, H2B, H3B, HR, R, RBI, SB, CS, SO, playerID):
        """
        Parameters
        ----------
        name : str
            The name of the player, first and last including suffix (e.g. Jr.)

        G : int
            The number of games played.

        PA : int
            number of PA

        AB : int
            at bats

        BB : int
            Walks

        H1B : int
            Singles

        H2B : int
            Doubles

        H3B : int
            Triples

        HR : int
            Home runs

        R : int
            Runs scored

        RBI : int 
            Runs batted in

        SB : int
            Stolen Bases

        CS : int 
            Caught stealing

        SO : int
            Strike outs

        playerID : string
            A player id, intended to be unique. Note, should not raise errors if set to a numeric value, but string is preferred.

        Raises
        ------
        ValueError
            If the numeric types are not passes as numeric.
        """
        try: ##verify the data is proper type:
            (G + PA + AB + H1B + H2B + H3B + HR + R + RBI + SB + CS + SO)
        except ValueError:
            raise ValueError("This object {} {} was created with non numeric types for numerical variables.".format(self,name))
            
        self.name = name
        self.games = G
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
        """
            This prints all the basic stats for a player. Currently, somewhat incomplete but can be used to inspect
            internal data for completeness.
            
        """
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
        """
        Normalizes all the players counting stats to a new number of PA.

        Parameters
        ----------
        PA : int
            The number of PA the player is adjusted to. 
            In order to prevent data loss, zero is not allowed and passing zero will have no effect.
            To approximate zero, pass a small float (.01) as PA.
        """
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
        """
        Returns a copy of the player, normalized to a number of plate appearnaces using adjToPA(pa).

        Parameters
        ----------
        pa : int
            The number of plate appearnaces to normalize to.
        """
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
        """Returns the players expected hits above replacement. Equal to (batting average - league batting average) * at bats.
            
            This is useful for figuring out whether the player provides value as a fantasy hitter. 
        """
        self.xH = (self.BA()-self.lgBA)*self.AB
        return self.xH
        
    def fWAR(self):
        """Returns standings points gained above replacement level. A fantasy baseball type of value measure similar to WAR.
        """
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
        """Returns fWAR without replacement level adjustment.
        """
        fWAR = self.HR/self.spgHR + self.RBI/self.spgRBI + self.R/self.spgR + self.SB/self.spgSB
        self.xH = self.calcxH()
        fWAR = fWAR + self.xH/self.spgxH ## - self.replacementLevel
        #if self.elig['C']:
        #    fWAR = fWAR +(16.72-12.59)
        ##print(fWAR)
        return fWAR


    def fWAR600(self):
        """The players fantasy value per 600 plate appearances, based one fWAR().
        """
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
        """
        Sets the value of elig[pos] to True.
        
        Parameters
        ----------
        pos : str
            A string used as a key in elig.


        """
        self.elig[pos]=True
                 
    def multiEligible(self):
        """
        Returns True if the player is eligible at multiple positions. Else, returns False.
        """
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
        """Returns a string of the positions abbreviations that the player is eligible at.

            Example: a player eligible at short stop and second base would return '2B SS'.
        """
        s = str()
        for key in self.elig:
            if self.elig[key]:
                s = s + " " + key
        return s

    def assistLine(self):
        """Returns a string 'box score' style line for the players fantasy relevant stats. 
        
            This is from an early version of this package and is not the preferred way to print this data.
        """
        guy = self
        team = guy.team
        if team == "Diamondbacks": #'Diamondbacks' is too long for formats.
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
        """
        Returns true if the player is a hitter. This is a hitter and returns true.
        Can be used to distinguish this as a hitter when the player is part of a group that includes 
        All players should have an isaHitter method. Pitchers should return false. 
        """
        return True

