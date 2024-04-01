from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.crud.ressource_crud import create_resource,get_resources
from app.scheme.ressource_scheme import ResourceCreate, ResourceDisplay
from app.dependencies.user import get_current_user
router = APIRouter()

@router.get("/", response_model=list[ResourceDisplay])
def read_resources(user_id: int=Depends(get_current_user), db: Session = Depends(get_db)):
    resources = get_resources(db, user_id=user_id)
    return resources

@router.post("/", response_model=ResourceDisplay)
def create(resource: ResourceCreate, user_id: int=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_resource(db=db, resource=resource, user_id=user_id)
