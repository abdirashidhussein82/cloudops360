
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Schema for incoming service creation requests
class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "active"
    environment: str = "development"


# Schema for outgoing service responses
class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    status: str
    environment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
# Schema for incoming service update requests
class ServiceUpdate(BaseModel):
    name: str
    description: str | None = None
    status: str
    environment: str