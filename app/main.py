
from app.schemas import ServiceCreate, ServiceResponse, ServiceUpdate
from app.database import get_db
from app import models

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

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


@app.get("/services", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    services = db.query(models.Service).all()

    return services


@app.post("/services", response_model=ServiceResponse, status_code=201)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = models.Service(**service.model_dump())

    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service


@app.put("/services/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service: ServiceUpdate,
    db: Session = Depends(get_db)
):
    db_service = db.query(models.Service).filter(
        models.Service.id == service_id
    ).first()

    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    for key, value in service.model_dump().items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)

    return db_service


@app.delete("/services/{service_id}", status_code=204)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    db_service = db.query(models.Service).filter(
        models.Service.id == service_id
    ).first()

    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(db_service)
    db.commit()
