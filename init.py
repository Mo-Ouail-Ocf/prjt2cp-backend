from sqlalchemy.orm import Session
from app.models import Resource
from app.core.database import engine
from typing import List
from pydantic import BaseModel
import json


class Module(BaseModel):
    code: str
    title: str
    ddc: str


class Pgm(BaseModel):
    id: str
    name: str
    modules: List[Module]


class PgmList(BaseModel):
    pgms: List[Pgm]


class Club(BaseModel):
    name: str
    description: str
    pfp_url: str


class ClubList(BaseModel):
    clubs: List[Club]


def init_module_list(db: Session) -> None:
    module = (
        db.query(Resource)
        .filter(Resource.type == "module")
        .filter(Resource.owner == None)
        .first()
    )
    if module is None:
        with open("./resources/module.json", "r") as f:
            data = json.load(f)
            pgm_list = PgmList.model_validate(data).pgms
            for pgm in pgm_list:
                level = pgm.name
                for module in pgm.modules:
                    resource = Resource(
                        name=module.code,
                        type="module",
                        level=level,
                        description=f"{module.ddc}: {module.title}",
                    )
                    db.add(resource)
    db.commit()


def init_club_list(db: Session) -> None:
    club = (
        db.query(Resource)
        .filter(Resource.type == "club")
        .filter(Resource.owner == None)
        .first()
    )
    if club is None:
        with open("./resources/club.json", "r") as f:
            data = json.load(f)
            clubs = ClubList.model_validate(data).clubs
            for club in clubs:
                resource = Resource(
                    name=club.name,
                    type="club",
                    description=club.description,
                    photo=club.pfp_url,
                )
                db.add(resource)
    db.commit()


def main() -> None:
    with Session(engine) as db:
        init_module_list(db)
        init_club_list(db)


if __name__ == "__main__":
    main()
