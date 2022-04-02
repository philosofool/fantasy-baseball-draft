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
