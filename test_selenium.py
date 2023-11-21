# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup



def iniciar_chrome():
    ruta = ChromeDriverManager().install()
    op = webdriver.ChromeOptions()
    # op.add_argument('--headless')
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    op.add_argument(f"user-agent={user_agent}")
    # op.add_argument("--window-size=100,1000")
    op.add_argument("--start-maximized")
    op.add_argument("--disable-web-security")
    op.add_argument("--disable-notifications")
    op.add_argument("--ignore-certificate-errors")
    op.add_argument("--no-sandbox")
    op.add_argument("--log-level=3")
    op.add_argument("--allow-running-insecure-content")
    op.add_argument("--no-default-browser-check")
    op.add_argument("--no-first-run")
    op.add_argument("--no-proxy-server")
    op.add_argument("--disable-blink-features=AutomationControlled")

    

    s=Service(ruta)
    driver  = webdriver.Chrome(service=s,options=op)
    return driver

if __name__=="__main__":
    driver=iniciar_chrome()
    url="https://www.pccomponentes.com/lenovo-ideapad-gaming-3-gen-6-intel-core-i5-11320h-16gb-512gb-ssd-gtx-1650-156"
    driver.get(url)

    input("pulsa enter")
    driver.quit()
