from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="CloudOps360 API",
    description="Enterprise Cloud Operations and Monitoring Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to CloudOps360",
        "platform": "Cloud Operations Platform",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "cloudops360",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }