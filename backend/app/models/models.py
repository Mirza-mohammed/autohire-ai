from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    preferences = Column(JSON, default={})
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    skills = Column(JSON, default=[])
    experience = Column(JSON, default=[])
    education = Column(JSON, default=[])
    master_resume_json = Column(JSON, default={})
    
    user = relationship("User", back_populates="profile")

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    title = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    extracted_reqs = Column(JSON, default={})
    source_url = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    job_id = Column(String, ForeignKey("job_postings.id"), nullable=False)
    status = Column(String, default="pending_review", index=True)
    applied_resume = Column(JSON, default={})
    match_score = Column(Float, default=0.0)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Analytics Fields
    tailoring_score = Column(Float, nullable=True) # Score assigned during AI tailoring
    time_to_apply = Column(Integer, nullable=True) # Time taken by Playwright in seconds
    outcome_reason = Column(String, nullable=True) # e.g. "Missing MLOps keywords"

    user = relationship("User", back_populates="applications")
    job = relationship("JobPosting", back_populates="applications")

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_type = Column(String, index=True, nullable=False) # e.g., "form_submitted", "bot_blocked"
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

