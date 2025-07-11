from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.database import Base

class ChatHistory(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, unique = True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    company = Column(String, nullable = False)
    job_role = Column(String, nullable = False)
    experience = Column(String, nullable = False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))