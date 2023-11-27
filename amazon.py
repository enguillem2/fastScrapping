from libs import *
import os
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time
from decouple import config
import pickle #para guardar cookies




url="https://amazon.es"

USER_AMZ = config("USER_AMZ")
PASS_AMZ = config("PASS_AMZ")


def login():
    if os.path.isfile("amazon.cookies"):
        print('Login por cookies')
        cookies = pickle.load(open("amazon.cookies","rb"))
        driver.get("https://amazon.es/robots.txt")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
        try:
            cursor_arriba()
            print('Login por cookies: ok')
            #elemento=wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR,"article")))
            return "ok"
        except TimeoutException:
            print("NO LOGIN COOKIES TIME")
            return "noOk"


    driver.get(url)

    #boto login
    elemento=wait.until(ec.visibility_of_element_located((By.ID,"nav-link-accountList")))
    elemento.click()
    # time.sleep(3)
    # input("wait")
    # elemento=driver.find_element(By.XPATH,"//span[contains(text(),'Identificarse')]")

    elemento=wait.until(ec.visibility_of_element_located((By.NAME,"email")))
    elemento.send_keys(USER_AMZ)

    elemento=wait.until(ec.visibility_of_element_located((By.ID,"continue")))
    elemento.click()

    elemento=wait.until(ec.visibility_of_element_located((By.NAME,"password")))
    elemento.send_keys(PASS_AMZ)
    elemento=wait.until(ec.visibility_of_element_located((By.ID,"signInSubmit")))
    elemento.click()

    cookies = driver.get_cookies()
    pickle.dump(cookies,open("amazon.cookies","wb"))
    print("cookies guardadas")



def preus(url):
    driver.get(url)
    time.sleep(4)
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    elements=driver.find_elements(By.CSS_SELECTOR,"div.ProductGridItem__item__IkSDt")
    print("elements: ",elements)
    for element in elements:
        try:
            titol=element.find_element(By.CSS_SELECTOR,"a.Title__title__z5HRm")
            # titol=items.find_element(By.CSS_SELECTOR,"a.Title__title__z5HRm Title__fixed__bJ2c2")
            print("titol:",titol.text)
            price=element.find_element(By.CSS_SELECTOR,"span.Price__price__LKpWT").get_attribute("aria-label")
            price=price.replace(u'\xa0', u' ').split(" ")[0].replace(',',".")
            price=float(price)
            print("price:",price)
            try:
                price_orig=element.find_element(By.CSS_SELECTOR,"span.Price__small__Y4NDm").get_attribute("aria-label")
                price_orig=float(price_orig.replace(u'\xa0', u' ').split(" ")[0].replace(',',"."))
            except:
                price_orig=0
            print("price_orig:",price_orig)
            if price_orig!=0:
                percent=100*price/price_orig
                print(f"percent {percent}%")
        except Exception as e :
            print("error!!!",e)




if __name__ == "__main__":
    driver=iniciar_chrome(headless=False,px=3000)
    wait= WebDriverWait(driver,10) #donam 10 segons pq es faci l'acció
    login()

    #sandisk
    preus("https://amzn.to/3RfmQ7z")

    #crucioal
    # url="https://amzn.to/3GhT2kz"
    preus("https://amzn.to/3GhT2kz")

    #test
    preus("https://www.amazon.es/stores/page/806A81D6-F27A-4402-A796-7FDACB52EDCD?ingress=0&visitId=d0afec7c-c114-4b6a-9705-dbd2d62f7c6f&lp_slot=auto-sparkle-hsa-tetris&store_ref=SB_A0933048PLB1IQ3HYI71&ref_=sbx_be_s_sparkle_lsi4d_cta")


    input("pres enter")
    driver.quit()