from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models import models
from app.schemas import schemas
from app.services.llm_service import llm_service, ExtractedJobRequirements

router = APIRouter()

# --- Users ---
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # In a real app, hash the password
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password_hash=fake_hashed_password, preferences=user.preferences)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# --- Profiles ---
@router.post("/users/{user_id}/profile/", response_model=schemas.Profile)
def create_profile_for_user(
    user_id: str, profile: schemas.ProfileCreate, db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.profile:
         raise HTTPException(status_code=400, detail="Profile already exists for this user")

    db_profile = models.Profile(**profile.model_dump(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.put("/profiles/{profile_id}", response_model=schemas.Profile)
def update_profile(
    profile_id: str, profile: schemas.ProfileCreate, db: Session = Depends(get_db)
):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for var, value in vars(profile).items():
        setattr(db_profile, var, value) if value is not None else None

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# --- Job Postings ---
@router.post("/jobs/", response_model=schemas.JobPosting)
def create_job_posting(job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.source_url == job.source_url).first()
    if db_job:
        raise HTTPException(status_code=400, detail="Job posting already exists")
    
    db_job = models.JobPosting(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/jobs/", response_model=List[schemas.JobPosting])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.JobPosting).offset(skip).limit(limit).all()
    return jobs

# --- Applications ---
@router.post("/users/{user_id}/applications/", response_model=schemas.Application)
def create_application(
    user_id: str, app: schemas.ApplicationCreate, db: Session = Depends(get_db)
):
    # Verify user and job exist
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == app.job_id).first()
    if db_job is None:
         raise HTTPException(status_code=404, detail="Job not found")

    # Check if already applied/pending
    existing_app = db.query(models.Application).filter(
        models.Application.user_id == user_id, 
        models.Application.job_id == app.job_id
    ).first()
    
    if existing_app:
        raise HTTPException(status_code=400, detail="Application already exists for this job")

    db_app = models.Application(
        user_id=user_id,
        job_id=app.job_id,
        status=app.status
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@router.get("/applications/", response_model=List[schemas.Application])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apps = db.query(models.Application).offset(skip).limit(limit).all()
    return apps

# --- AI Auto-Tailor ---
@router.post("/jobs/{job_id}/tailor/{user_id}", response_model=schemas.Application)
def auto_tailor_and_apply(job_id: str, user_id: str, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not db_profile or not db_profile.master_resume_json:
        raise HTTPException(status_code=400, detail="User profile or master resume not found")

    # 1. Parse Job Description if not already parsed
    if not db_job.extracted_reqs:
        extracted = llm_service.parse_job_description(db_job.description)
        db_job.extracted_reqs = extracted.model_dump()
        db.commit()

    # 2. Tailor Resume
    reqs = ExtractedJobRequirements(**db_job.extracted_reqs)
    tailored_resume = llm_service.tailor_resume(db_profile.master_resume_json, reqs)
    
    # 3. Generate Cover Letter
    cover_letter = llm_service.generate_cover_letter(
        master_resume_json=db_profile.master_resume_json,
        job_description=db_job.description,
        company_name=db_job.company_name,
        role_title=db_job.title
    )
    
    # Save to Application
    application_data = {
        "resume": tailored_resume.model_dump(),
        "cover_letter": cover_letter
    }
    
    # Check existing application
    db_app = db.query(models.Application).filter(
        models.Application.user_id == user_id, 
        models.Application.job_id == job_id
    ).first()
    
    if not db_app:
        db_app = models.Application(user_id=user_id, job_id=job_id, status="ready_for_review")
        db.add(db_app)
        
    db_app.applied_resume = application_data
    db_app.status = "ready_for_review"
    db.commit()
    db.refresh(db_app)
    
    return db_app
