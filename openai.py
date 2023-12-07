import os
import sys
import time
import pickle
import tempfile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys #per pulsar tecles
from iniciar_webdriver_uc import iniciar_webdriver

from decouple import config
from lib.colors import *


class ChatGPT:
    def __init__(self,user,password):
        self.OPENAI_USER=user   
        self.OPENAI_PASS=password
        self.COOKIES_FILE=f'{tempfile.gettempdir()}/openai.cookies'
        print(f'{azul}Iniciando webdriver{gris}')
        self.driver = iniciar_webdriver(headless=False,pos="right")
        self.wait= WebDriverWait(self.driver,30)
        login = self.login_openai()
        print()
        if not login:
            sys.exit(1)
        
    def login_openai(self):

        #login por cookies
        if os.path.isfile(self.COOKIES_FILE):
            print(f'\33[K{azul}login por cookies... {gris}')
            cookies = pickle.load(open(self.COOKIES_FILE,"rb"))
            print(f'\33[K{azul}cargando robots.txt... {gris}')
            self.driver.get("https://chat.openai.com/robots.txt")
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            self.driver.get("https://chat.openai.com")
            login=self.comprobar_login()
            if login:
                print(f'\33[K{azul}LOGIN DESDE cookies: {verde}OK{gris}')
            else:
                print(f'\33[K{azul}LOGIN DESDE cookies: {rojo}FALLIDO{gris}')
            return login








        print(f'\33[K{azul}LOGIN DESDE CERO {gris}')
        print(f'\33[K{azul}cargando chatGPT... {gris}')
        self.driver.get("https://chat.openai.com")
        cursor_arriba()
        print(f'\33[K{azul}click en login... {gris}')
        elemento=self.wait.until(ec.visibility_of_element_located((By.XPATH,"//div[text()='Log in']")))
        elemento.click()

        cursor_arriba()
        print(f'\33[K{azul}introduciendo usuario... {gris}')
        elemento=self.wait.until(ec.visibility_of_element_located((By.NAME,"username")))
        elemento.send_keys(self.OPENAI_USER)
        elemento.send_keys(Keys.ENTER)

        cursor_arriba()
        print(f'\33[K{azul}introduciendo password... {gris}')
        elemento=self.wait.until(ec.visibility_of_element_located((By.NAME,"password")))
        elemento.send_keys(self.OPENAI_PASS)
        elemento.send_keys(Keys.ENTER)

        login=self.comprobar_login()

        if login:
            #guardam cookies
            pickle.dump(self.driver.get_cookies(),open(self.COOKIES_FILE,"wb"))
            print(f'\33[K{azul}LOGIN DESDE ZERO: {verde}OK{gris}')
        else:
            print(f'\33[K{azul}LOGIN DESDE ZERO: {rojo}FALLIDO{gris}')

            

        return login
    
    def comprobar_login(self,tiempo=30):
        login = False
        while tiempo>0:
            print(tiempo)
            try: 
                e = self.driver.find_element(By.CSS_SELECTOR,"textarea[tabindex='0']")
                e.click()
                login = True
                break
            except:
                pass

            try:
                #sesion expirada
                e=self.driver.find_element(By.CSS_SELECTOR,"h3.text-lg")
                if "session has expired" in e.text:
                    cursor_arriba()
                    print(f'\33[K{amarillo}LA SESIÓN HA EXPIRADO{gris}')
                    print()
                    break
            except:
                pass

            time.sleep(1)
            tiempo=tiempo-1
            cursor_arriba()
            borrar_linea()

        return login
    
    def chatear(self,prompt):
        print(prompt)
        elemento=self.driver.find_element(By.CSS_SELECTOR,"textarea[tabindex='0']")
        elemento.send_keys(prompt)
        elemento.send_keys(Keys.ENTER)
        respuesta=""
        time.sleep(3)
        inicio= time.time()
        generating=True
        while generating:
            try:
                buttons=self.driver.find_elements(By.CSS_SELECTOR,"button.rounded-full")
                generating=False
                for b in buttons:
                    label=b.get_attribute('aria-label')
                    if label=="Stop generating":
                        generating=True
                    
            except:
                if respuesta:
                    break
            e = self.driver.find_elements(By.CSS_SELECTOR,"div.markdown")[-1]
            respuesta=e.text
            segundos=int(time.time()-inicio)
            if segundos:
                cursor_arriba()
                print(f'\33[K{azul}generando respuesta... {gris}{segundos} segundos ({len(respuesta)})')
                time.sleep(1)
                cursor_arriba()
                borrar_linea()
        e = self.driver.find_elements(By.CSS_SELECTOR,"div.markdown")[-1]
        respuesta=e.text
        return respuesta
    
    def cerrar(self):
        print(f'\33[K{azul} cerrando... {gris}')
        self.driver.quit()

                

        

if __name__ == "__main__":
    OPENAI_USER = config("OPENAI_USER")
    OPENAI_PASS= config("OPENAI_PASS")
    chat=ChatGPT(OPENAI_USER,OPENAI_PASS)
    prompt=""
    prompt=input("pregunta: ")
    while prompt!="salir":
        respuesta=chat.chatear(prompt)
        print(f'\33[K{amarillo}{respuesta}{gris}')
        prompt=input("pregunta: ")
    chat.cerrar()
    sys.exit()