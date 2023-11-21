# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup



def iniciar_chrome():
    ruta = ChromeDriverManager().install()
    s=Service(ruta)
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    

    driver  = webdriver.Chrome(service=s,options=op)
    url="https://www.pccomponentes.com/lenovo-ideapad-gaming-3-gen-6-intel-core-i5-11320h-16gb-512gb-ssd-gtx-1650-156"
    driver.get(url)

if __name__=="__main__":
    iniciar_chrome()