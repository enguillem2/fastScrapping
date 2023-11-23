from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys #per pulsar tecles

import os
import wget
from decouple import config

from pathlib import Path

import pickle #para guardar cookies

USER_IG = config("USER_IG")
PASS_IG = config("PASS_IG")

print(USER_IG,PASS_IG)

