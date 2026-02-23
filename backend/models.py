from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
import database

class Report(database.Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    message = Column(Text)
    extracted_url = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
