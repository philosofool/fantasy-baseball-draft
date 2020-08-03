import numpy as np

class StatCalculator:
    '''Provides basic functionality for getting rate and counting stats from existing stats.
    
    Includes pre-defined calculator for common and fantasy-relevant stats.

    Class Attributes
    ----------
    Note: it is strongly recommned that users modify the class attributes rather
    instance
    lgERA: numeric
    The league's era. Note that default is keyed to a fantasy stat.

    Setting the attributes on instances may result in inconsistent
    applications of the spg function across multiple instances.

    spg: dict (string: numeric)
    The standings points gained (SPG) coefficients for basic fantsay stats. Keys are 'HR', 'W', etc.

    lgBA: numeric
    The league's batting average

    replacement_level: dict (string: numeric)
    The raw SPG value for each player who is replacement level at their position.

    '''

    team_name_to_city_abbr = {
    'Angels': 'LAA','Astros':'HOU', 'Dodgers':'LAD',
    'Indians': 'CLE', 'Brewers': 'MIL', 'Athletics':'OAK',
    'Twins': 'MIN', 'White Sox' : 'CHW', 'Nationals': 'WAS',
    'Red Sox': 'BOS', 'Padres':'SD', 'Cubs' : 'CHC',
    'Rockies': 'COL', 'Yankees': 'NYY', 'Braves': 'ATL',
    'Phillies': 'PHI', 'Diamondbacks': 'ARI', 'Cardinals': 'STL',
    'Blue Jays':'TOR', 'Mets': 'NYM', 'Reds': 'CIN',
    'Rays': 'TB', 'Marlins': 'MIA', 'Royals':'KC',
    'Rangers': 'TEX', 'Pirates': 'PIT', 'Mariners': 'SEA',
    'Giants' : 'SF',  'Tigers': 'DET', 'Orioles': 'BAL'
    }

    spg = {
        'K': 17.5,
        'xER': 8.5,
        'xWHIP': 12.4,
        'W': 1.7,
        'S': 4.5,
        'SB': 3.5,
        'HR': 5.3,
        'xH': 8.5,
        'RBI': 13.4,
        'R': 11.7
        }
    lgERA = 3.79
    lgWHIP = 1.23
    replacement_level = pd.Series{
        'P': 11.4,
        'C': 9,
        '1B': 16.7,
        '2B': 16.7,
        '3B': 16.7,
        'SS': 16.7,
        'OF': 16.7,
        'RF': 16.7,
        'CF': 16.7,
        'LF': 16.7,
        'U': 16.7,
        }

    spgxH = 8.475##used 8.47, nearly matched the real value of 8.486 in 2019.
    spgHR = 5.286##real value was 4.782
    spgR = 11.671###used 10.81,real value was 12.532
    spgRBI = 13.38##used 12.20,was 14.564
    spgSB = 3.46##used 4.27,was 2.657
    lgBA = .265

    _standard_pitching_keys = {i : i for i in ['K','W','S','ER','IP','BB','H','ERA','WHIP']}
    _standard_hitting_keys = {i : i for i in ['H','HR','R','RBI','SB','BA','AB']}

    def __init__(self):
        pass

    @staticmethod
    def from_rate(rate, denominator, to_int=False):
        '''
        Returns a counting-type stat from a rate and a denominator.
        
        Note: this is essentially the product of the two arguments.

        You might be wondering: so, why? You certainly don't have to! It's mostly for coherence
        and the idea that this is "all you need for your baseball maths" in a single
        place. Note that get_rate (the complement of this function) allows us to decide whether to 
        allow infitie values instead of handling a division by zero error. When coupled with pandas,
        this gives us a good way impute stats via df.replace(inf,df['ERA'].mean()) for example.
        '''
        out = rate * denominator
        if to_int:
            out = int(round(out))
        return out

    @staticmethod
    def get_rate(numerator, denominator, to_int=False, allow_inf=True):
        '''
        Returns a rate stat, e.g. K/IP, from arguments, with options to handle division by zero.
        
        '''
        out = np.divide(numerator,denominator)
        if not allow_inf:
            if out == np.inf:
                raise ZeroDivisionError("Denominator in getRate was zero. Try 'allow_inf' = True")
        if to_int:
            try:
                out = int(round(out))
            except OverflowError:
                pass
        return out

    @staticmethod
    def Kper9(pitcher_stats, stat_dict=None, allow_inf = True):
        '''
        Returns strikeouts per nine innnings from a dict-like of pitcher stats.

        Parameters
        ----------
        pitcher_stats: dict_like 
        
        Pitcher stats that includes strikeouts and innings pitched.

        stat_dict: dictionary, default = None

        A dictionary mapping 'K' and/or 'IP' to names for those stats in pitcher_stats or None. Used when pitcher_stats uses names
        besides 'K' and 'IP' for strikeouts and innings pitched. If None, uses 'K' and 'IP' as pitcher_stats keys.
        '''
        
        if not stat_dict:
            return getRate(pitcher_stats['K'], pitcher_stats['IP']/9, allow_inf=allow_inf)
        else:
            stat_dict = {**_standard_pitching_keys, **stat_dict}
            K = pitcher_stats(stat_dict['K'])
            IP = pitcher_stats(stat_dict['IP'])
            return getRate(K,IP/9, allow_inf = allow_inf)

    @staticmethod
    def normalize_IP(IP):
        '''
        Converts IP with .1 or .2 to 1/3 and 2/3 respectively. 
        '''
        whole_IP = int(IP)
        partial_IP = IP%1 * 10/3
        return whole_IP + partial_IP

    @staticmethod
    def BBper9(pitcher_stats, stat_dict=None, allow_inf = True):
        '''
        Returns walks per nine innnings from a dict-like of pitcher stats.

        Parameters
        ----------
        pitcher_stats: dict_like 
        
        Pitcher stats that includes walks and innings pitched.

        stat_dict: dictionary, default = None

        A dictionary mapping 'BB' and/or 'IP' to the names used for those in pitcher_stats, or None. Use if pitcher_stats uses names
        besides 'BB' and 'IP' for walks and innings pitched. If None, uses 'BB' and 'IP' as pitcher_stats keys.
        '''
        if not stat_dict:
            return getRate(pitcher_stats['BB'], pitcher_stats['IP']/9, allow_inf = allow_inf)
        else:
            stat_dict = {**_standard_pitching_keys, **stat_dict}
            BB = pitcher_stats[stat_dict['BB']]
            IP = pitcher_stats[stat_dict['IP']]
            return getRate(BB,IP/9, allow_inf = allow_inf)

    def FIP(self, pitcher_stats, fip_const = 3.20, stat_dict = None):
        if not stat_dict:
            K = pitcher_stats['K']
            BB = pitcher_stats['BB']
            IP = pitcher_stats['IP']
            HR = pitcher_stats['HR']
        else:
            stat_dict = {**_standard_pitching_keys, **stat_dict}
            K = pitcher_stats[stat_dict['K']]
            BB = pitcher_stats[stat_dict['BB']]
            IP = pitcher_stats[stat_dict['IP']]
            HR = pitcher_stats[stat_dict['HR']]
        FIP = np.divide((3*BB - 2*K + 13 * HR),IP) + fip_const
        return FIP

    def pitcherFWAR(self, pitcher_stats, position = 'P', use_count_stats = True, stat_dict = None):
        '''
        Returns a cummulative SPG value, adjusted for replacement level, from a pitcher's stats.
        
        Parameters
        ----------
        pitcher_stats: dict_like
            A list of pitcher stats that includes strikeouts, walks, hits, earned runs, innings pitched, wins, and saves. 
        
        position: string, default = 'P'
            A string for the player's positon. Used to calculate replacement level value.
        
        use_count_stats: bool, default = True
            Use counting stats (ER, W, H) for calculations if True; use rate stats (ERA, WHIP) if False.

        stat_dict: dictionary, default = None
            A dictionary map of standard keys to the keys used for those stats in player_stats. 
            The standard keys are 'W', 'S', 'K', 'BB', 'IP', 'H', 'ER', 'ERA', 'WHIP'. This can be
            a partial map; standard keys are used when stat_dict contains no entry for that stat.
        

        '''
        if use_count_stats:
            if not stat_dict:
                K = pitcher_stats['K']
                W = pitcher_stats['W']
                S = pitcher_stats['S']
                ER = pitcher_stats['ER']
                BB = pitcher_stats['BB']
                H = pitcher_stats['H']
                IP = pitcher_stats['IP']
                RA = H + BB #RA = runners allowed.
            else:
                stat_dict = {**self._standard_pitching_keys, **stat_dict}
                K = pitcher_stats[stat_dict['K']]
                W = pitcher_stats[stat_dict['W']]
                S = pitcher_stats[stat_dict['S']]
                ER = pitcher_stats[stat_dict['ER']]
                BB = pitcher_stats[stat_dict['BB']]
                H = pitcher_stats[stat_dict['H']]
                IP = pitcher_stats[stat_dict['IP']]
                RA = H + BB
        else:
            if not stat_dict:
                K = pitcher_stats['K']
                W = pitcher_stats['W']
                S = pitcher_stats['S']
                ER = pitcher_stats['ERA']*pitcher_stats['IP']/9
                RA = pitcher_stats['WHIP']*pitcher_stats['IP']
                IP = pitcher_stats['IP']
            else:
                stat_dict = {**self._standard_pitching_keys, **stat_dict}
                K = pitcher_stats[stat_dict['K']]
                W = pitcher_stats[stat_dict['W']]
                S = pitcher_stats[stat_dict['S']]
                IP = pitcher_stats['IP']
                ER = pitcher_stats[stat_dict['ERA']]*IP/9
                RA = pitcher_stats['WHIP']*IP
                
        K_ = K/self.spg['K']
        W_ = W/self.spg['W']
        S_ = S/self.spg['S']
        xER_ = ((self.lgERA * IP) - ER)/self.spg['xER']
        xWHIP_ = ((self.lgWHIP * IP) - (RA))/self.spg['xWHIP']
        return K_ + W_ + S_ + xER_ + xWHIP_ - self.replacement_level[position]

    def hitterFWAR(self, hitter_stats, position = 'U', use_replacement = True, use_count_stats = True, stat_dict = None):
        '''
        Returns a cummulative SPG value, adjusted for replacement level, from a hitter's stats.
        ##FIX ME
        Current documentation incomplete. See pitcherFWAR for some guidance.
        '''
        if use_count_stats:
            if not stat_dict:
                HR = hitter_stats['HR']
                SB = hitter_stats['SB']
                RBI = hitter_stats['RBI']
                R = hitter_stats['R']
                H = hitter_stats['H']
                AB = hitter_stats['AB']
            else:
                stat_dict = {**self._standard_hitting_keys, **stat_dict}
                HR = hitter_stats[stat_dict['HR']]
                SB = hitter_stats[stat_dict['SB']]
                RBI = hitter_stats[stat_dict['RBI']]
                R = hitter_stats[stat_dict['R']]
                H = hitter_stats[stat_dict['H']]
                AB = hitter_stats[stat_dict['AB']]

        else:
            if not stat_dict:
                HR = hitter_stats['HR']
                SB = hitter_stats['SB']
                RBI = hitter_stats['RBI']
                R = hitter_stats['R']
                AB = hitter_stats['AB']
                H = hitter_stats['BA']*AB
            else:
                stat_dict = {**self._standard_hitting_keys, **stat_dict}
                HR = hitter_stats[stat_dict['HR']]
                SB = hitter_stats[stat_dict['SB']]
                RBI = hitter_stats[stat_dict['RBI']]
                R = hitter_stats[stat_dict['R']]
                AB = hitter_stats[stat_dict['AB']]
                H = hitter_stats[stat_dict['BA']]*AB
                
        HR_ = HR/self.spg['HR']
        RBI_ = RBI/self.spg['RBI']
        R_ = R/self.spg['RBI']
        SB_ = SB/self.spg['SB']
        xH_ = (H - self.lgBA*AB)/self.spg['xH']
        if use_replacement:
            rep_level = self.replacement_level[position]
        else:
            rep_level = 0
        return HR_ + RBI_ + R_ + SB_ + xH_ - rep_level

    def calc_hitter_replacement_level(self, data, count = 180, use_count_stats=True, stat_dict=None):
        fwar_series = data.apply(self.hitterFWAR(data, 
                                                 use_count_stats = use_count_stats, stat_dict=stat_dict,
                                                 use_replacement = False))
        return min(fwar_series.nlargest(count))






