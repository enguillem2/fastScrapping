from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys #per pulsar tecles
from selenium.webdriver.common.by import By

from libs import *
import os
import sys
import wget
from decouple import config

from pathlib import Path

import pickle #para guardar cookies
import time
import wget
url="https://flickr.com"

USER_IG = config("USER_IG")
PASS_FLK = config("PASS_IG")

def login():
    #no cookies
    driver.get(url)
    # elemento=wait.until(ec.visibility_of_element_located((By.XPATH,"//button[contains(text(),'Permitir todas')]")))
    # elemento.click()
def descargar_fotos(hashtag,max):
    pass


if __name__ == "__main__":
    MINIMO=100
    #control de params
    print(f"len(sys.argv): {len(sys.argv)}")
    if len(sys.argv) == 1 or len(sys.argv)>3:
        print("error parametres")
        sys.exit(1)
    elif len(sys.argv) == 3:
        if sys.argv[2].isdigit():
            MINIMO=int(sys.argv[2])
        else:
            print(f'error: {sys.argv[2]} no es un número')

    HASHTAG = sys.argv[1].strip("#")
    print(f'HASHTAG: {HASHTAG} MINIMO: {MINIMO}')
    driver=iniciar_chrome(headless=False,px=3000)
    wait= WebDriverWait(driver,10) #donam 10 segons pq es faci l'acció
    res = login()
    res = descargar_fotos(HASHTAG,MINIMO)
    input("pres enter")
    driver.quit()