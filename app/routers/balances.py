from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.balance import BalanceResponse
from app.services.balance_service import calculate_group_balances
from app.utils.dependencies import get_current_user
from app.services.simplify_service import simplify_balances


router = APIRouter(prefix="/balances", tags=["Balances"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/group/{group_id}", response_model=list[BalanceResponse])
def get_group_balances(
    group_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return calculate_group_balances(group_id, db)

@router.get("/group/{group_id}/simplified")
def get_simplified_group_balances(
    group_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    raw = calculate_group_balances(group_id, db)
    return simplify_balances(raw)

