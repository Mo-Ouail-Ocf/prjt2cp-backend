from pydantic import BaseModel
from typing import Optional

class ResourceCreate(BaseModel):
    name: str
    type: str
    level: Optional[str] = None
    description: Optional[str] = None

class ResourceDisplay(BaseModel):
    resource_id: int
    name: str
    type: str
    level: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes=True
