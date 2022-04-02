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
