from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.api import endpoints, analytics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoHire AI API")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1/analytics")

@app.get("/")
def read_root():
    return {"message": "Welcome to AutoHire AI API"}
