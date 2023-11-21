import requests
from bs4 import BeautifulSoup

url="https://www.game.es/game-hx500-rgb-71-pro-gaming-headset-pc-ps4-auriculares-auriculares-gaming-pc-hardware-169628"
url="https://www.game.es/ACCESORIOS/AURICULARES/PC-GAMING/RAZER-KAIRA-FOR-PS5-PS4-PC-MOVIL-AURICULARES-INALAMBRICOS/V1FFP2"
headers={"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

if __name__ == "__main__":
    res = requests.get(url,headers=headers)
    print(res.status_code)

    soup = BeautifulSoup(res.text,"html.parser")
    print(soup.title.text)
    product_title=soup.find("h2",class_="product-title").text.strip()
    print(product_title)

    product_price=soup.find("div",class_="buy--price")
    print(product_price)
    product_price_int=product_price.find("span",class_="int").text.strip()
    product_price_dec=product_price.find("span",class_="decimal").text.strip()
    product_price_currency=product_price.find("span",class_="currency").text.strip()
    print("enter:",product_price_int+","+product_price_dec.split("'")[1]+product_price_currency)
