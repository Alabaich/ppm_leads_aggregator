from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Lead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_leads(db: Session = Depends(get_db)):
    """
    Returns all leads for the React Dashboard.
    """
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return leads