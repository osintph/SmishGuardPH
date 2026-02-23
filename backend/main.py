from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import re
import database, models

# Ensure tables are created
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmishGuard PH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY: API KEY SETUP ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Pull the secret key from the .env file, fallback to a default if missing
VALID_API_KEY = os.getenv("API_KEY", "bayanihan_secret_key_2026")

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key_header
# -------------------------------

class ReportCreate(BaseModel):
    sender: str
    message: str

@app.post("/api/report")
def create_report(report: ReportCreate, db: Session = Depends(database.get_db)):
    urls = re.findall(r'(https?://[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)', report.message)
    extracted_url = urls[0] if urls else "No URL detected"
    
    new_report = models.Report(
        sender=report.sender, 
        message=report.message, 
        extracted_url=extracted_url
    )
    db.add(new_report)
    db.commit()
    return {"status": "success", "extracted_url": extracted_url}

# We secure this endpoint by passing the `get_api_key` dependency
@app.get("/api/feed")
def get_feed(api_key: str = Depends(get_api_key), db: Session = Depends(database.get_db)):
    reports = db.query(models.Report).order_by(models.Report.timestamp.desc()).limit(50).all()
    return {"threat_feed": reports}
import urllib.request
import xml.etree.ElementTree as ET

# --- NEW: Philippine Cyber News Endpoint ---
@app.get("/api/news")
def get_ph_cyber_news():
    # Fetches real-time PH cybersecurity and data privacy news via Google News RSS
    url = "https://news.google.com/rss/search?q=Philippines+cybersecurity+OR+%22Data+Privacy+Act%22+OR+smishing&hl=en-PH&gl=PH&ceid=PH:en"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        news_items = []
        
        # Grab the top 4 latest news articles
        for item in root.findall('.//item')[:4]: 
            # Clean up the title (Google News appends the publisher at the end)
            raw_title = item.find('title').text
            title = raw_title.rsplit(' - ', 1)[0] if ' - ' in raw_title else raw_title
            
            news_items.append({
                "title": title,
                "link": item.find('link').text,
                "pubDate": item.find('pubDate').text
            })
        return {"status": "success", "news": news_items}
    except Exception as e:
        print(f"Error fetching news: {e}")
        return {"status": "error", "news": []}