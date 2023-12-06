from fastapi import FastAPI

# from app.server.models import ScrapeRequest
# from app.server.scraping import do_scraping


app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

# @app.post("/scrape")
# async def scrape_url(request: ScrapeRequest):
#     # Lógica para realizar scraping
#     data = do_scraping(request.url)
#     return {"data": data}