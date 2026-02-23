from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import re
import database, models

# Auto-create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmishGuard PH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReportCreate(BaseModel):
    sender: str
    message: str

@app.post("/api/report")
def create_report(report: ReportCreate, db: Session = Depends(database.get_db)):
    # Basic RegEx to parse URLs from the scam message
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

@app.get("/api/feed")
def get_feed(db: Session = Depends(database.get_db)):
    # Returns the latest 50 threats for the open-source feed
    reports = db.query(models.Report).order_by(models.Report.timestamp.desc()).limit(50).all()
    return {"threat_feed": reports}
