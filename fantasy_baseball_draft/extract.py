"""Tools for fetching baseball data from the internet."""

import yaml
import shutil
import os
import pandas as pd

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import utils

from functionals.utils import sequential_compose

config_path = os.path.normpath('../settings/config.yml')

with open() as yml:
    config = yaml.safe_load(yml.read())
#assert config['password']
#assert config['username']

def nav_to_cbs(browser: Firefox) -> Firefox:
    """Login to CBS and load main page.
    
    This authenticates a headless browser for successive calls."""
    browser.get("https://www.cbssports.com/login?product_abbrev=mgmt&xurl=https%3A%2F%2Fklf2006.baseball.cbssports.com%2F&master_product=38994")
    user = browser.find_element_by_id('userid')
    password = browser.find_element_by_id('password')
    button = browser.find_element_by_name('_submit')
    user.send_keys(config['username'])
    password.send_keys(config['password'])
    button.click()
    return browser

def download_cbs_hitters(browser) -> Firefox:
    """Download cbs hitters."""    
    batter_true_talent = "https://klf2006.baseball.cbssports.com/stats/stats-main/all:C:1B:2B:3B:SS:MI:CI:LF:CF:RF:U/ytd:p/True+Talent?"
    browser.get(batter_true_talent)
    browser.find_element(By.ID, 'btnExport').click()
    save_as = f'cbs_hitters_{pd.Timestamp.now().strftime("%Y-%m-%d")}'
    move_download_to_data(save_as)
    return browser

def _move_download_to_data(new_name) -> None:
    import shutil
    f = get_most_recent_file(config['download_dir'])
    shutil.move(
        os.path.join(config['download_dir'], f),
        os.path.join(config['data_dir'], new_name)
    )

#move_download_to_data('test_batter_tt.csv')

# File utils. 

def get_most_recent_file(directory) -> str:
    """Return name of most recent file in dir."""
    times = get_files_creation_times(directory)
    return times[max(times.keys())]

def get_files_creation_times(directory) -> dict:
    """Map file names to creation times."""
    c_time = lambda f: os.path.getctime(os.path.join(directory, f))
    return {c_time(f): f for f in os.listdir(directory)}
    