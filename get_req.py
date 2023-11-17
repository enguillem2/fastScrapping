import requests

h={"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

url="https://amzn.to/3G1Wboz"
res = requests.get(url,headers=h)

print(res.reason)
print(res.cookies)

with open("static/codigo_200.html","w",encoding="utf-8") as f:
    f.write(res.text)