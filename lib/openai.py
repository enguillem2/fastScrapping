import os
import sys
import time
import pickle
import tempfile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys #per pulsar tecles
from lib.colors import *
from lib.iniciar_webdriver_uc import iniciar_webdriver
from bs4 import BeautifulSoup

# from iniciar_webdriver_uc import iniciar_webdriver

from decouple import config


class ChatGPT:
    def __init__(self,user,password,headless=False):
        self.OPENAI_USER=user   
        self.OPENAI_PASS=password
        # self.COOKIES_FILE=f'{tempfile.gettempdir()}/openai.cookies'
        self.COOKIES_FILE=f'lib/openai.cookies'

        print(f'{azul}Iniciando webdriver{negro}')
        self.driver = iniciar_webdriver(headless=headless,pos="right")
        self.wait= WebDriverWait(self.driver,30)
        login = self.login_openai()
        print("login fet")
        if not login:
            sys.exit(1)
        
    def login_openai(self):
        print(os.path.isfile(self.COOKIES_FILE))

        #login por cookies
        if os.path.isfile(self.COOKIES_FILE):
            print(f'\33[K{azul}login por cookies... {negro}')
            cookies = pickle.load(open(self.COOKIES_FILE,"rb"))
            print(f'\33[K{azul}cargando robots.txt... {negro}')
            self.driver.get("https://chat.openai.com/robots.txt")
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                    print(f'{verde}cookie {cookie["name"]}{gris}')
                except:
                    pass
            url="https://chat.openai.com"
            print(f'{verde}carga url {url} {gris}')
            self.driver.get(url)
            login=self.comprobar_login()
            # login=True
            if login:
                print(f'\33[K{azul}LOGIN DESDE cookies: {verde}OK{negro}')
            else:
                print(f'\33[K{azul}LOGIN DESDE cookies: {rojo}FALLIDO{negro}')
            return login








        print(f'\33[K{azul}LOGIN DESDE CERO {negro}')
        print(f'\33[K{azul}cargando chatGPT... {negro}')
        self.driver.get("https://chat.openai.com")
        cursor_arriba()
        print(f'\33[K{azul}click en login... {negro}')
        elemento=self.wait.until(ec.visibility_of_element_located((By.XPATH,"//div[text()='Log in']")))
        elemento.click()

        cursor_arriba()
        print(f'\33[K{azul}introduciendo usuario... {negro}')
        elemento=self.wait.until(ec.visibility_of_element_located((By.NAME,"username")))
        elemento.send_keys(self.OPENAI_USER)
        elemento.send_keys(Keys.ENTER)

        cursor_arriba()
        print(f'\33[K{azul}introduciendo password... {negro}')
        elemento=self.wait.until(ec.visibility_of_element_located((By.NAME,"password")))
        elemento.send_keys(self.OPENAI_PASS)
        elemento.send_keys(Keys.ENTER)

        login=self.comprobar_login()

        if login:
            #guardam cookies
            pickle.dump(self.driver.get_cookies(),open(self.COOKIES_FILE,"wb"))
            print(f'\33[K{azul}LOGIN DESDE ZERO: {verde}OK{negro}')
        else:
            print(f'\33[K{azul}LOGIN DESDE ZERO: {rojo}FALLIDO{negro}')

            

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
                    print(f'\33[K{amarillo}LA SESIÓN HA EXPIRADO{negro}')
                    print()
                    break
            except:
                pass

            time.sleep(1)
            tiempo=tiempo-1
            cursor_arriba()
            borrar_linea()

        return login
    
    def chatear(self,prompt,formato="string"):
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
                print(f'\33[K{azul}generando respuesta... {negro}{segundos} segundos ({len(respuesta)})')
                time.sleep(1)
                cursor_arriba()
                borrar_linea()
        e = self.driver.find_elements(By.CSS_SELECTOR,"div.markdown")[-1]
        if formato=="string":
            respuesta=e.text
        elif formato=="html":
            respuesta=self.formato_html()
        return respuesta
    
    def formato_html(self):
        #parsearmos la pagina
        def cambiar_etiquetas(texto):
            texto=texto.replace('<p>','').replace('</p>','')
            texto=texto.replace('<li>','').replace('</li>','')

            texto=texto.replace('<strong>','<b>').replace('</strong>','</b>')
            texto=texto.replace('<em>','<i>').replace('</em>','</i>')
            texto=texto.replace('<del>','<s>').replace('</del>','</s>')


            return texto
        
        def html_tg_code(texto):
            return texto.replace('<','&lt;').replace('>','&gt;')

        salida=""
        soup=BeautifulSoup(self.driver.page_source,"html.parser")
        respuesta = soup.find_all("div",{"class":"markdown"})[-1]

        for x in respuesta.contents:
            tag = x.name
            if tag == "p":
                texto=str(x)
                texto = cambiar_etiquetas(texto)

                salida+=f'{texto}\n\n'
            elif tag=="pre":
                texto=x.find("code").text
                salida+=f'<code>{html_tg_code(texto)}</code>\n'
            elif tag=="ol":
                n=x.attrs.get("start")
                if n:
                    n=int(n)
                else:
                    n=1
                for y in x.contents:
                    texto = y.find("p")
                    if not texto:
                        texto=y

                    if "li" in texto:
                        lista=texto.split('</li>')
                        for item in lista:
                            if item:
                                texto=item.replace('<li>','')
                                texto = cambiar_etiquetas(texto)
                                salida+=f'- {texto}\n'
                    
                    salida+=f'{n}. {cambiar_etiquetas(str(texto))}\n'
                    texto = y.find("pre")
                    if texto:
                        texto= y.find("code").text
                        salida+=f'<code>{html_tg_code(texto)}</code>\n'
                    n+=1
                    salida+="\n"
            elif tag=="ul":
                texto=str(x)
                texto=texto.replace('<ul>','').replace('</ul>','')
                lista=texto.split('</li>')
                for item in lista:
                    if item:
                        texto=item.replace('<li>','')
                        texto = cambiar_etiquetas(texto)
                        salida+=f'- {texto}\n'



        return salida


    
    def cerrar(self):
        print(f'\33[K{azul} cerrando... {negro}')
        self.driver.quit()

                

        

if __name__ == "__main__":
    OPENAI_USER = config("OPENAI_USER")
    OPENAI_PASS= config("OPENAI_PASS")
    chat=ChatGPT(OPENAI_USER,OPENAI_PASS)
    prompt=""
    prompt=input("pregunta: ")
    while prompt!="salir":
        respuesta=chat.chatear(prompt)
        print(f'\33[K{amarillo}{respuesta}{negro}')
        prompt=input("pregunta: ")
    chat.cerrar()
    sys.exit()