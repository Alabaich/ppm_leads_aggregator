import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 1. Connection: Uses the URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Model: The Lead Table
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow) # System timestamp

    # Core Prospect Info
    prospect_name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, nullable=True)
    
    # Source Info
    source = Column(String, nullable=True)               # Generic Source (e.g. "RentSync")
    integration_source = Column(String, nullable=True)   # Specific ILS (e.g. "Zumper")
    
    # Property Info
    inquiry_date = Column(DateTime, nullable=True)
    property_name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    beds = Column(String, nullable=True)
    baths = Column(String, nullable=True)
    
    # New Mapping Columns
    move_in_date = Column(String, nullable=True)         # Mapping "moveInDate"
    promotion = Column(String, nullable=True)            # Mapping "promotionType"
    
    # Status
    status = Column(String, default="New", index=True)
    
    # Debugging Columns
    debug_1 = Column(Text, nullable=True)
    debug_2 = Column(Text, nullable=True)

# 3. Init Function
def init_db():
    Base.metadata.create_all(bind=engine)