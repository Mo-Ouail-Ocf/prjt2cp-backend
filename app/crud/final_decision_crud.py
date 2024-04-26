from sqlalchemy.orm import Session
from app.models import FinalDecision
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
