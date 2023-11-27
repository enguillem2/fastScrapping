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
url="https://instagram.com"

USER_IG = config("USER_IG")
PASS_IG = config("PASS_IG")


def descargar_fotos_instagram(hashtag,minimo):
    print(f'buscando fotos de #{hashtag}')
    url=f"https://instagram.com/explore/tags/{hashtag}"
    driver.get(url)
    elemento=driver.find_element(By.CSS_SELECTOR,"html")
    #scroll
    for n in range(20):
        print("pagedown")
        time.sleep(1)
        elemento.send_keys(Keys.PAGE_DOWN)

def login_insta():
    print("login en insta")
    raya()
    if os.path.isfile("instagram.cookies"):
        print('Login por cookies')
        cookies = pickle.load(open("instagram.cookies","rb"))
        driver.get("https://instagram.com/robots.txt")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
        try:
            cursor_arriba()
            print('Login por cookies: ok')
            elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"article")))
            return "ok"
        except TimeoutException:
            print("NO LOGIN COOKIES TIME")
            return "noOk"

        return "ok"
    
    #no cookies
    driver.get(url)
    elemento=wait.until(ec.visibility_of_element_located((By.XPATH,"//button[contains(text(),'Permitir todas')]")))
    elemento.click()

    try:
        username=wait.until(ec.visibility_of_element_located((By.NAME,"username")))
        password=wait.until(ec.visibility_of_element_located((By.NAME,"password")))
        username.send_keys(USER_IG)
        password.send_keys(PASS_IG)

    except TimeoutException:
        print('erro no user name')
        return "error"


    try:
        log=wait.until(ec.visibility_of_element_located((By.XPATH,"//div[contains(text(),'Entrar')]")))
        time.sleep(2)
        log.click()

        elemento = wait.until(ec.visibility_of_element_located((By.XPATH,"//button[contains(text(),'Guardar información')]")))
        elemento.click()
        elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"article")))
    except TimeoutException:
        print("error click")
        return "error"
    
    cookies = driver.get_cookies()
    pickle.dump(cookies,open("instagram.cookies","wb"))
    print("cookies guardadas")




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
    res = login_insta()
    res = descargar_fotos_instagram(HASHTAG,MINIMO)
    input("pres enter")
    driver.quit()


