from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base
from sqlalchemy.types import Float

class Intent(Base):
    __tablename__ = "intents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float, nullable=False)
    raw_input = Column(String, nullable=False)

    def __repr__(self):
        return f"<Intent(id={self.id}, name='{self.name}', confidence='{self.confidence}', raw_input='{self.raw_input}')>"