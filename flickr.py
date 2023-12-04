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
url="https://identity.flickr.com/login?redir=https%3A%2F%2Fflickr.com%2F"

USER_FLK = config("USER_FLK")
PASS_FLK = config("PASS_FLK")

def login():
    
    if os.path.isfile("flickr.cookies"):
        url="https://flickr.com"
        print('Login por cookies')
        cookies = pickle.load(open("flickr.cookies","rb"))
        driver.get("https://identity.flickr.com/login?redir=https%3A%2F%2Fflickr.com%2F")
        for cookie in cookies:
            print("cokie",cookie)
            driver.add_cookie(cookie)
        driver.get(url)
        try:
            cursor_arriba()
            print('Login por cookies: ok')
            elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"body")))
            return "ok"
        except TimeoutException:
            print("NO LOGIN COOKIES TIME")
            return "noOk"

    
    
    #no cookies
    driver.get(url)
    # elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"a.acceptAll")))
    # elemento.click()

    
    
    
    input("wait")
    # elemento=wait.until(ec.visibility_of_element_located((By.XPATH,"//a[contains(text(),'Iniciar sesión')]")))
    # elemento.click()

    elemento=wait.until(ec.visibility_of_element_located((By.ID,"login-email")))
    elemento.send_keys(USER_FLK)

    elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"span.user-select-none")))
    elemento.click()
    
    elemento=wait.until(ec.visibility_of_element_located((By.ID,"login-password")))
    elemento.send_keys(PASS_FLK)

    elemento=wait.until(ec.visibility_of_element_located((By.XPATH,"//span[contains(text(),'Iniciar sesión')]")))
    elemento.click()

    cookies = driver.get_cookies()
    pickle.dump(cookies,open("flickr.cookies","wb"))
    print("cookies guardadas")





    # iframe=driver.find_element(By.TAG_NAME("iframe"))
    # print(f"iframe: {iframe}")

    # elemento=driver.find_element(By.CSS_SELECTOR,"body")
    # links=elemento.find_elements(By.CSS_SELECTOR,"a")
    # i=0
    # for l in links:
    #     i+=1
    #     print(i,l.text)
    #     if l.text=="Iniciar sesión":
    #         break
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