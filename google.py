from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys #per pulsar tecles
from selenium.webdriver.common.by import By

from lib.openai import ChatGPT
from lib.iniciar_webdriver_uc import iniciar_webdriver


from libs import *
import os
import sys
import wget
from decouple import config

from pathlib import Path

import pickle #para guardar cookies
import time
import tempfile


url="https://google.com"

USER_GLG = config("USER_GLG")
PASS_GLG= config("PASS_GLG")


def login():
    #no cookies
    url="https://google.com"


    # if os.path.isfile("google.cookies"):
    #     print('Login por cookies')
    #     cookies = pickle.load(open("google.cookies","rb"))
        
    #     driver.get("https://google.com/robots.txt")
    #     for cookie in cookies:
    #         print(cookie)
    #         driver.add_cookie(cookie)
    #     driver.get(url)
    #     try:
    #         cursor_arriba()
    #         print('Login por cookies: ok')
    #         elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"body")))
    #         return "ok"
    #     except TimeoutException:
    #         print("NO LOGIN COOKIES TIME")
    #         return "noOk"

    #     return "ok"

    driver.get("https://google.com")
    print("getting google")

    elemento=wait.until(ec.visibility_of_element_located((By.XPATH,"//div[text()='Aceptar todo']")))
    elemento.click()

    url="https://accounts.google.com"
    driver.get(url)
    # elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"a.acceptAll")))
    # elemento.click()
    elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"input[type='email']")))
    elemento.send_keys(USER_GLG)
    elemento.send_keys(Keys.ENTER)

    elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"input[type='password']")))
    elemento.send_keys(PASS_GLG)
    elemento.send_keys(Keys.ENTER)

    

    # driver.get("https://google.com")
    # print("getting google")

    
    cookies = driver.get_cookies()
    pickle.dump(cookies,open("google.cookies","wb"))
    print("cookies guardadas")

def search(hashtag):
    url=f"https://www.google.com/search?q={hashtag}"
    driver.get(url)


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
    driver=iniciar_webdriver(headless=False,pos="right")
    wait= WebDriverWait(driver,10) #donam 10 segons pq es faci l'acció
    res = login()
    # res = search(HASHTAG)

    input("pres enter")
    driver.get("https://chat.openai.com")
    input("pres enter")
    COOKIES_FILE=f'{tempfile.gettempdir()}/openai.cookies'

    pickle.dump(driver.get_cookies(),open(COOKIES_FILE,"wb"))


    driver.quit()