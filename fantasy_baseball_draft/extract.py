"""Tools for fetching baseball data from the internet."""

import yaml
import shutil
import os
import pandas as pd

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import utils

class Extractor:
    def __init__(self, config):
        self.config = config
        self.browser = self.set_browser()
        #self.nav_to_cbs()
        
    @classmethod
    def from_config_path(cls, path):
        with open(path) as yml:
            return cls(yaml.safe_load(yml.read()))

    def set_browser(self):
        opts = Options()
        opts.headless = True
        return Firefox(options=opts)
    
    def _move_download_to_data(self, new_name) -> None:
        f = get_most_recent_file(self.config['download_dir'])
        shutil.move(
            os.path.join(self.config['download_dir'], f),
            os.path.join(self.config['data_dir'], new_name)
        )

    def nav_to_cbs(self):
        """Login to CBS and load main page.
        
        This authenticates a headless browser for successive calls."""

        self.browser.get(self.config['cbs_home'])
        user = self.browser.find_element_by_id('userid')
        password = self.browser.find_element_by_id('password')
        button = self.browser.find_element_by_name('_submit')
        user.send_keys(self.config['username'])
        password.send_keys(self.config['password'])
        button.click()

    def download_data(self, target, path):
        self.browser.get(target)
        self.browser.find_element(By.ID, 'btnExport').click()
        self._move_download_to_data(path)

    def download_cbs_hitters(self):
        """Download cbs hitters."""    
        self.download_data(
            self.config['cbs_hitters'], 
            f'cbs_hitters_{pd.Timestamp.now().strftime("%Y-%m-%d")}.csv'
        )

    def download_cbs_pitchers(self):
        """Download cbs pitchers."""
        self.download_data(
            self.config['cbs_pitchers'],
            f'cbs_pitchers_{pd.Timestamp.now().strftime("%Y-%m-%d")}.csv'
        )

    def _move_download_to_data(self, new_name) -> None:
        f = get_most_recent_file(self.config['download_dir'])
        shutil.move(
            os.path.join(self.config['download_dir'], f),
            os.path.join(self.config['data_dir'], new_name)
        )

# File utils. 

def get_most_recent_file(directory) -> str:
    """Return name of most recent file in dir."""
    times = get_files_creation_times(directory)
    return times[max(times.keys())]

def get_files_creation_times(directory) -> dict:
    """Map file names to creation times."""
    c_time = lambda f: os.path.getctime(os.path.join(directory, f))
    return {c_time(f): f for f in os.listdir(directory)}
    