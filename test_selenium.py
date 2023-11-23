# selenium 3
from libs import iniciar_chrome

from selenium.webdriver.common.by import By





if __name__=="__main__":
    driver=iniciar_chrome()
    url="https://www.pccomponentes.com/grandstream-dp720-telefono-inalambrico-voip"
    # url="https://www.pccomponentes.com/aoc-24g2spae-bk-238-led-ips-fullhd-165hz-freesync-premium"
    # url="https://www.pccomponentes.com/lenovo-ideapad-gaming-3-gen-6-intel-core-i5-11320h-16gb-512gb-ssd-gtx-1650-156"
    # url="https://www.pccomponentes.com/alurin-go-start-intel-celeron-n4020-8gb-256gb-ssd-156"
    driver.get(url)
    nombre_producto = driver.find_element(By.ID,"pdp-title").text 
    original_price = driver.find_elements(By.ID,"pdp-price-original-sticky")
    price_sell = driver.find_element(By.ID,"pdp-price-current-integer-sticky").text
    print(f"NOMBRE PRODUCTO: {nombre_producto}")
    print(f"original price: {original_price}")
    print(f"price sell: {price_sell}")

    input("PULSA ENTER")
    driver.quit()
