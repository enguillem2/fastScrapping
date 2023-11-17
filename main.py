from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models import ScrapeRequest
from scraping import do_scraping

app = FastAPI()

# Montar el directorio de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/scrape")
async def scrape_url(request: ScrapeRequest):
    # Lógica para realizar scraping
    data = do_scraping(request.url)
    return {"data": data}
