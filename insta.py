from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys #per pulsar tecles
from selenium.webdriver.common.by import By

from libs import iniciar_chrome
import os
import wget
from decouple import config

from pathlib import Path

import pickle #para guardar cookies
import time
url="https://instagram.com"

USER_IG = config("USER_IG")
PASS_IG = config("PASS_IG")

def login_insta():
    print("login en insta")
    driver.get(url)
    elemento=driver.find_element(By.XPATH,"//button[contains(text(),'Permitir todas')]")
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
    except TimeoutException:
        print("error click")
        return "error"







def login_instagram():
    if os.path.isfile("instagram.cookies"):
        print("hi ha cookies")
        cookies = pickle.load(open("instagram.cookies","rb"))
        driver.get("https://instagram.com/robots.txt")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://instagram.com")
        try:
            print('Login por cookies: ok')
            # elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"article[role='presentation']")))
            boton=wait.until(ec.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Permitir todas las cookies')]")))
            boton.click()
            return "ok"
        except TimeoutException:
            print("NO LOGIN COOKIES TIME")

        return "ok"
    
    print("no hi ha cookies")
    driver.get("https://www.instagram.com")
    boton=wait.until(ec.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Permitir todas las cookies')]")))
    boton.click()
    
    name=wait.until(ec.visibility_of_element_located((By.NAME,"username")))
    password=wait.until(ec.visibility_of_element_located((By.NAME,"password")))

       
    name.send_keys(USER_IG)
    password.send_keys(PASS_IG)

    try:
        submit=wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']")))
        submit.click()

        elemento=wait.until(ec.element_to_be_clickable((By.XPATH,"//button[text()='Save Info']")))
        elemento.click()
        elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"article[role='presentation']")))
        print('Login desde cero: ok')
    except TimeoutException:
        print("feed de noticias no cargado")
        return "error"
    # guardam cookies amb pickle
    cookies = driver.get_cookies()
    pickle.dump(cookies,open("instagram.cookies","wb"))
    print("cookies guardadas")



if __name__ == "__main__":

    driver=iniciar_chrome(headless=False,px=3000)
    wait= WebDriverWait(driver,10) #donam 10 segons pq es faci l'acció
    res = login_insta()

    input("pres enter")
    driver.quit()


