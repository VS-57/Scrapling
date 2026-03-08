from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from scrapling.fetchers import StealthyFetcher
import uvicorn
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="Scraper API")
executor = ThreadPoolExecutor(max_workers=3)

def fetch_html_sync(url: str):
    # Verilen adrese gidiyoruz (Cloudflare'i aşarak)
    page = StealthyFetcher.fetch(
        url,
        headless=True,
        network_idle=True
    )
    # body HTML bytes objesi döndürür, utf-8'e çeviriyoruz.
    return page.body.decode('utf-8', errors='ignore')

@app.get("/api/scrape", response_class=HTMLResponse)
async def get_html(url: str = Query(..., description="The URL to scrape")):
    try:
        loop = asyncio.get_running_loop()
        html_content = await loop.run_in_executor(executor, fetch_html_sync, url)
        return html_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="[IP_ADDRESS]", port=8000, reload=True)
