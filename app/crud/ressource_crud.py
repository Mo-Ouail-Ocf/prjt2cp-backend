# resource_crud.py
from sqlalchemy.orm import Session
from app.models.resource import Resource
from app.scheme.ressource_scheme import ResourceCreate


def get_resources(db: Session, user_id: int):
    return (
        db.query(Resource)
        .filter((Resource.owner_id == user_id) | (Resource.owner_id.is_(None)))
        .all()
    )


def create_resource(db: Session, resource: ResourceCreate, user_id: int):
    db_resource = Resource(**resource.model_dump(), owner_id=user_id)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource