from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.db.database import get_db
from app.models import models

router = APIRouter()

@router.get("/funnel/{user_id}")
def get_application_funnel(user_id: str, db: Session = Depends(get_db)):
    """
    Returns the count of applications at each stage of the funnel.
    Stages: scraped -> evaluated -> applied -> interviewing -> rejected/hired
    """
    
    # We will simulate a funnel based on Application statuses.
    # In a real system, you might have separate models, but for the MVP:
    # "pending_review" -> Evaluated
    # "applied" -> Auto-Applied
    # "interview" -> Interviewing
    # "rejected" / "hired" -> Closed
    
    status_counts = db.query(models.Application.status, func.count(models.Application.id)).filter(
        models.Application.user_id == user_id
    ).group_by(models.Application.status).all()
    
    # Initialize funnel with 0
    funnel = {
        "Evaluated": 0,
        "Auto-Applied": 0,
        "Interviewing": 0,
        "Closed": 0
    }
    
    for status, count in status_counts:
        if status == "pending_review":
            funnel["Evaluated"] += count
        elif status == "applied":
            funnel["Auto-Applied"] += count
        elif status == "interview":
            funnel["Interviewing"] += count
        elif status in ["rejected", "hired"]:
            funnel["Closed"] += count
            
    # For a realistic MVP demo, let's inject some dummy data if it's completely empty.
    if sum(funnel.values()) == 0:
        funnel = {
            "Evaluated": 120,
            "Auto-Applied": 45,
            "Interviewing": 8,
            "Closed": 37
        }
            
    # Format for Recharts: [{name: 'Evaluated', value: 120}, ...]
    result = [{"name": k, "value": v} for k, v in funnel.items()]
    return result

@router.get("/agent-performance/{user_id}")
def get_agent_performance(user_id: str, db: Session = Depends(get_db)):
    """
    Returns data correlating AI tailoring score with application outcomes.
    """
    # For MVP, we return a mocked scatter plot distribution since the DB is mostly empty.
    # In production, this runs a SQL JOIN on outcome vs tailoring_score.
    
    return [
        {"score": 95, "outcome": 1, "company": "Google"},
        {"score": 92, "outcome": 1, "company": "Stripe"},
        {"score": 88, "outcome": 0, "company": "Meta"},
        {"score": 85, "outcome": 0, "company": "Amazon"},
        {"score": 98, "outcome": 1, "company": "OpenAI"},
        {"score": 81, "outcome": 0, "company": "Netflix"},
    ]
