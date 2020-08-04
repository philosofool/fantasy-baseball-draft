import numpy as np
import pandas as pd

class NameToFangraphsID:
    """ 
    A tool for mapping name data with Fangraphs playerids. 
    
    The expected use includes having a collection of data without unique baseball playerids
    and adding ids from another collection of data. This can then be used to merge data sets.
    Presumably, a player's name provides a partial column on which to join. This class
    provides some functionality to handle duplication of names and naming variations. 
    
    Attributes
    ----------
    
    fg_data: DataFrame
        A DataFrame that includes unique player ids.
    
    name_data: DataFrame
        A DataFrame that includes data without unique player ids or with
        ids that don't match those in fg_data.
        
    fg_name: string
        The name for column containing data, such as a player's name, which can be identified
        similar data in the other data. 
        
    fg_pid: string
        The name for columns with a unique id.
        
    name_player: string
        The name of a column from which a match to name data can be found. Used for 
        extracting name data.
        
    empty_value: any
        The default value written when no data is provided.
        
    extract_func: function
        A function used to extract name data from other data.
        
    Methods
    -------
    extract_name(name_data)
        Extracts data from a string; used to find string matches with player names, for example.
    
    fg_name_id_map()
        Returns a dictionary that maps names in fg_data to playerids.
    
    transform_suffix(suffix, add=True):
        Adds or removes a suffix from names in name_data.
        
    transform_name(dictionary, name_data_key = None):
        Transforms names in name_data by mapping with a dictionary. Names that don't match a dictionary key
        are ignored.
        
    duplicated_names(in_names = True, as_series = True):
        Returns a Series or list of the names which are duplicated in the data.
                
    duplicated_name_entries(in_names =True):
        Returns a DataFrame of all entries with a duplicate name value.
    
    add_ids_from_dict(dictionary, name_data_key = None):
        Add playerids to name_data from a dictionary that has playerids as values.
        
    add_ids_from_fg_data(fg_on= True, name_data_on= True):
        Adds playerids to name_data using a columns from fg_data and name_data as a dictionary key.
        
    get_name_data_dict(name_data_key):
        Returns a dictionary mapping a column from name_data to playerids.

    """
    
    def __init__(self, fg_data, name_data, fg_data_name= 'Name', fg_data_pid= 'playerid', 
                 name_data_col= 'Player', empty_value= np.nan, extract_name_func = 'default'):
        """
        Parameters
        ----------
        fg_data: DataFrame or str
            The data including unique player ids. If string, string name of a csv file. If a DataFrame,
            the data is copied and not a view.
        
        name_data: DataFrame or str
            The data without unique player ids. If string, should name a csv file. If a DataFrame, the data
            is copied and not a view.
            
        fg_data_pid: str
            The name of a column in which playerid data is written and found. default 'playerid'
            
        name_data_col: str
            The name of a column in name_data from which a name can be extracted. Default = 'Player'
        
        empty_value: any
            The value to write when no data exists. Default is numpy.nan.
        
        extract_name_func: function or 'default'
            The function used to extract name data from name_data_col. If 'default', uses the 
            default lambda function. (See method docs for extract_name)
        """
        ## FIX ME
        ## Currently, if the name_data includes a column with a name == fg_data_name, this will
        ## overwrite the name_data[fg_data_name].
        
        try:
            self.fg_data = pd.read_csv(fg_data)
        except ValueError:
            self.fg_data = fg_data.copy()
        try:
            self.name_data = pd.read_csv(name_data)
        except:
            self.name_data = name_data.copy()
        self.fg_name = fg_data_name
        self.fg_pid = fg_data_pid
        self.name_player = name_data_col
        self.empty_value = empty_value
        self.name_data[self.fg_pid] = self.empty_value
        self.name_data[self.fg_name] = self.empty_value
        if extract_name_func == 'default':
            self.extract_func = (lambda x: ' '.join(x.strip().split()[:-3]))
            #self.extract_func = (lambda x: x)
        else:
            self.extract_func = extract_name_func
        self.name_data[self.fg_name] = self.name_data[self.name_player].apply(self.extract_name)
        self.name_data[self.fg_pid] = np.nan
        #self.name_data['Name'] = self.name_data['Player'].apply(self.extract_name)   
        
    def extract_name(self, name_data):
        """
        Extracts data from a string; used to find string matches with player names, for example.
        
        The assumed input value is from a CBS Fantasy Baseball File. These have the form of:
            Ichiro Suzuki CF | SEA
        and this method returns everything before the ' CF'.
        
        The end user can assign a function to self.extrac_func to replace default behavior with something else that
        suits the data they have. Currently, support is limited to single argument functions.
        
        Parameters
        ----------
        
        name_data: str
            A string from which a name can be extracted.
        
        Examples
        --------
        
        Example of assigning another fucntion to this name: For a trivial case where 
        name_data is just a name but might include white space:
            >>> NameToFangraphsID.extract_name_name = (lambda x: x.strip())
        More complex functions can be defined, but can only accept one argument.
        """
        
        return self.extract_func(name_data)
    
    def fg_name_id_map(self):
        '''
        Returns a dictionary that maps fangraphs names to playerids.
        '''
        return dict(zip(self.fg_data[self.fg_name],self.fg_data[self.fg_pid]))
    
    def transform_suffix(self, suffix, add=True):
        '''
        Adds or removes a suffix from names in name_data. Default is add.
        
        Addition adds the suffix to a names in name_data if it matches fg_data names
        without the suffix. Removal removes the suffix and any whitespace preceding it.
        
        This transformation applies to duplicated names. 
        
        Parameters
        ----------
        
        suffix: str
            The string to add or remove.
        
        add: bool
            Whether to add the string to the name data or remove it. 
        '''
        if add:
            series = self.fg_data[self.fg_name]
            suffixed = series.where(series.str.endswith(suffix)).dropna()
            suffix_map = { name.replace(suffix,'').strip() : name for name in suffixed }
            ## Possible improvement? It feels a little silly and is probably slow.
            ## Using apply on a whole data frame when a single column is being transformed.
            ## Better would be Series.map with a defaultdict.
            ## Later...
            self.name_data = self.name_data.apply(self._apply_dict,
                                                  args=(suffix_map,
                                                       self.fg_name,
                                                       self.fg_name), axis=1)
        else:
            name_data[self.fg_name] = name_data[self.fg_name].apply(lambda x: x.replace(suffix,''))
            
    def transform_names(self, dictionary, name_data_key = None):
        '''
        Transforms names in name_data with a dictionary. Names that don't match a dictionary key
        are ignored.
        
        Parameters
        ----------
        
        dictionary: dict
            The dictionary that will be used to transform names
            
        name_data_key: immutable
            The name of the column in which to find the keys in the dictionary. By default this is
            the name of the columns in which the name data is found in fg_data.
        '''
        if not name_data_key:
            name_data_key = self.fg_name
            
        self.name_data = self.name_data.apply(self._apply_dict, args=(dictionary,
                                                                      name_data_key,
                                                                      self.fg_name), axis=1)
                                              
    def duplicated_names(self, in_names = True, as_series = True):
        """
        Returns a series or list of the names which are duplicated in the data.
        
        Parameters
        ----------
        
        in_names: bool
            If true, finds duplicated names in name_data. If false, finds duplicated
            names in fg_data.
            
        as_series: bool
            Determines the type of the return value. A pandas series if True; a list if False.
            
        Returns
        -------
            A series or list containing the names that are repeated. A series will share indices
            with the DataFrame from which it is derived.
        """
        
        if in_names:
            out = self.name_data[self.fg_name]
        else:
            out = self.fg_data[self.fg_name]
        out = out[out.duplicated(keep=False)]
        if as_series:
            return out
        else:
            return list(out)
        
    def duplicated_name_entries(self, in_names =True): 
        """
        Returns a DataFrame of the entries that are duplicated names.
        
        This function can be useful for identifying which names need to be handled
        and for developing functions to handle them.
        
        Parameters
        ----------
        in_names: bool
            The duplicated entries in name_data, if True. The duplicated entries in fg_data
            if False.
             
        Returns
        -------
            A view of the DataFrame entries that have duplicated names.
        """
        if in_names:
            mask = self.name_data.duplicated(subset=self.fg_name, keep = False)
            return self.name_data[mask]
        else:
            mask =  self.fg_data.duplicated(subset=self.fg_name, keep = False)
            return self.fg_data[mask]
        
    
    def add_ids_from_dict(self, dictionary, name_data_key = None):
        '''
        Add playerids to name_data from a dictionary that has playerids as values.
        
        Parameters
        ----------
        dictionary: dict
            A dicitonary that maps a column in name_data to playerids
            
        name_data_key: immutable
            The name of a column in name_data; the data elements are passed as keys to dictionary.
        '''
        if not name_data_key:
            name_data_kay = self.fg_name
        self.name_data = self.name_data.apply(self._apply_dict,
                                              args = (dictionary,
                                                     name_data_key,
                                                     self.fg_pid), axis=1)
        
    def add_ids_from_fg_data(self, fg_on= True, name_data_on= True):
        '''
        Adds playerids to name_data using a column from fg_data and name_data as a dictionary key.
        
        Constructs a dictionary of {key: playerid} from the fg_data using column named with fg_on. Then
        applies that dictionary by finding keys in name_data from name_data_on to add player ids to name_data. 
        
        Parameters
        ----------
        fg_on: bool or str
            Column containing data used as dictionary keys for a mapping. Uses fg_name if true. This data
            should match some data in the column of name_data_on.
        
        name_data_on: bool or str
            Column containing data use as dictionary keys for a mapping. Uses fg_name if true. This data
            should match some data in the column of fg_on.
            
        
        '''
        if fg_on == True:
            fg_on = self.fg_name
        if name_data_on == True:
            name_data_on = self.fg_name
        dictionary = dict(zip(self.fg_data[fg_on],self.fg_data[self.fg_pid]))
        self.name_data = self.name_data.apply(self._apply_dict, args = (dictionary,
                                                                       name_data_on,
                                                                       self.fg_pid), axis=1)
        
    def get_name_data_dict(self, name_data_key):
        """
        Returns a dictionary mapping a column from name_data to playerids.
        
        Parameters
        ----------
        
        name_data_key: str
            The column name used as keys in name_data.
            
        Returns
        -------
        
        dict: 
            A dicionary containing keys from a column in name_data and values that are playerids. 
        """
        return dict(zip(self.name_data[name_data_key],self.name_data[self.fg_pid]))
                                              
    
    def _apply_dict(self,row,dictionary,key,value):
        '''
        use dictionary to map row[key] to vow[value], ignoring KeyError Exceptions.
        '''
        #print("Applying dict....")
        #print(row)
        #print()
        #print(dictionary)
        #print(key)
        #print(value)
        #print(temp)
        row[key]## throw an expection if the row doesn't have the keys.
        row[value] ## or if the row doesn't have the values
        try:
            row[value] = dictionary[row[key]]
        except KeyError: #the dictionary doesn't have an entry key == row[key]
            pass
        return row