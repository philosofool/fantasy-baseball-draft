import pandas as pd

class Pitchers:
    '''
    Class for handling pitcher statistics. Functionality includes aggregating and merging stat sets.
    '''
    def __init__(self, df, csv=False, skiprows = 0):
        if csv:
            df = pd.read_csv(df, skiprows = skiprows)
        self.df = df





