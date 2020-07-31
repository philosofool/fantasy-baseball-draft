import pandas as pd

class Pitchers:
    '''
    Class for handling pitcher statistics. Functionality includes aggregating and merging stat sets.

    
    '''
    def __init__(self, df, csv=False, skiprows = 0):
        if csv:
            df = pd.read_csv(df, skiprows = skiprows)
        self.data = df

    def add_availability(self, cbs_file):


    def aggregate_with(self, agg_df, weight=0.5, drop_ignored=False, inplace=False):
        """Creates a DataFrame that combines stats from this an another DataFrame
        
        Parameters
        ----------

        agg_df: DataFrame
            A DataFrame to average with existing data. 

        weight: float
           The weighting applied to the native data. The result for stat named 'x'
           will be weight*self['x'] + (1-weight)*agg_df['x']. (Default = 0.5)

        drop_ignored: bool
            Whether to include values in the original DataFrame that have no entry in agg_df. 
        """






