# selenium 3
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def iniciar_chrome(headless=True):
    ruta = ChromeDriverManager().install()
    op = webdriver.ChromeOptions()
    if headless:
        op.add_argument('--headless')
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    op.add_argument(f"user-agent={user_agent}")
    op.add_argument("--window-size=100,1000")
    # op.add_argument("--start-maximized")
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
    #parametros a omitir
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-loggin'
    ]
    op.add_experimental_option("excludeSwitches",exp_opt)
    #preferencias
    prefs={
        "profile.default_content_settings_value.notifications": 2,
        "intl.accept_languages":["es-ES", "es"],
        "credentials_enable_service":False
    }
    op.add_experimental_option("prefs",prefs)

    

    s=Service(ruta)
    driver  = webdriver.Chrome(service=s,options=op)
    return driver

if __name__ == "__main__":
    driver=iniciar_chrome()
    driver.quit()