from typing import Annotated
from fastapi import APIRouter, Depends
from app.crud.final_decision_crud import get_final_decisions
from app.dependencies import get_db
from app.dependencies import valid_session_user
from app.scheme.final_decision_scheme import FinalDecisionResponse
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/session/{session_id}", response_model=list[FinalDecisionResponse])
async def get_final_decisions_of_session(
    _: Annotated[int, Depends(valid_session_user)],
    session_id: int,  # no need to check
    db: Session = Depends(get_db),
):
    return get_final_decisions(db, session_id)
