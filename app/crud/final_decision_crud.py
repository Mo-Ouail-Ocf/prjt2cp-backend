from sqlalchemy.orm import Session
from app.models import FinalDecision, Session
from app.scheme.final_decision_scheme import FinalDecisionCreate


def create_final_decision(
    db: Session, final_decision_data: FinalDecisionCreate
) -> FinalDecision:
    final_decision = FinalDecision(**final_decision_data.model_dump())
    db.add(final_decision)
    db.commit()
    db.refresh(final_decision)
    return final_decision


def get_final_decisions(db: Session, session_id: int) -> list[FinalDecision]:
    return db.query(FinalDecision).filter(FinalDecision.session_id == session_id).all()


def update_final_decision(
    db: Session, new_session_id: int, final_decision_id: int
) -> FinalDecision:
    final_decision = (
        db.query(FinalDecision)
        .filter(FinalDecision.decision_id == final_decision_id)
        .first()
    )
    final_decision.new_session_id = new_session_id
    db.add(final_decision)
    db.commit()
    return final_decision


def is_valid_final_decision(db: Session, final_decision_id: int, project_id: int):
    final_decision = (
        db.query(FinalDecision)
        .filter(FinalDecision.decision_id == final_decision_id)
        .first()
    )
    if final_decision is None:
        return False

    session = (
        db.query(Session)
        .filter(Session.session_id == final_decision.session_id)
        .first()
    )

    return session.project_id == project_id
