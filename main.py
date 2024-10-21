# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.auth import verify_token
from app.scraper_selenium import Scraper
from app.notification_strategies.console_notification import ConsoleNotification

app = FastAPI()

class ScrapeInput(BaseModel):
    page_limit: int = None
    proxy: str = None

@app.post("/scrape/")
async def scrape_data(scrape_input: ScrapeInput, token: str = Depends(verify_token)):
    scraper = Scraper(scrape_input.page_limit, scrape_input.proxy, notification_strategy=ConsoleNotification())
    scraped_products = scraper.scrape_products()
    return {"message": f"Scraped {len(scraped_products)} products", "products": scraped_products}
