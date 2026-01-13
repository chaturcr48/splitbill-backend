from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from decimal import Decimal
from typing import List, Optional
from app.database import SessionLocal
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.group_member import GroupMember
from app.models.user import User
from app.models.group import Group
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import List, Optional

@router.get("", response_model=List[ExpenseResponse])
def get_expenses(
    group_id: Optional[int] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Start query selecting the Expense object AND the Group name
    query = db.query(Expense, Group.name.label("expenses_group_name")).join(
        Group, Expense.group_id == Group.id
    )
    
    if group_id:
        # Check membership for the specific group
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id
        ).first()
        
        if not member:
            raise HTTPException(status_code=403, detail="Not a group member")
        
        query = query.filter(Expense.group_id == group_id)
    else:
        # Get all groups user belongs to
        user_groups = select(GroupMember.group_id).where(
            GroupMember.user_id == current_user.id
        )
        query = query.filter(Expense.group_id.in_(user_groups))
    
    # 2. Execute query
    results = query.order_by(Expense.created_at.desc()).all()
    
    # 3. Map the (Expense, group_name) tuples to your response format
    # This combines the expense data with the extra field
    return [
        {
            **expense.__dict__, 
            "group_name": group_name
        } 
        for expense, group_name in results
    ]


# @router.get("", response_model=List[ExpenseResponse])
# def get_expenses(
#     group_id: Optional[int] = None,
#     current_user = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(Expense)
    
#     if group_id:
#         member = db.query(GroupMember).filter(
#             GroupMember.group_id == group_id,
#             GroupMember.user_id == current_user.id
#         ).first()
        
#         if not member:
#             raise HTTPException(status_code=403, detail="Not a group member")
        
#         query = query.filter(Expense.group_id == group_id)
#     else:
#         user_groups = select(GroupMember.group_id).where(
#             GroupMember.user_id == current_user.id
#         )
#         query = query.filter(Expense.group_id.in_(user_groups))
    
#     expenses = query.order_by(Expense.created_at.desc()).all()
#     return expenses

@router.post("", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == expense.group_id)
        .all()
    )

    member_ids = {m.user_id for m in members}
    if current_user.id not in member_ids:
        raise HTTPException(status_code=403, detail="Not a group member")

    for uid in expense.split_between:
        if uid not in member_ids:
            raise HTTPException(status_code=400, detail="Invalid split member")

    new_expense = Expense(
        group_id=expense.group_id,
        paid_by=current_user.id,
        amount=expense.amount,
        description=expense.description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    share = Decimal(expense.amount) / Decimal(len(expense.split_between))

    for uid in expense.split_between:
        split = ExpenseSplit(
            expense_id=new_expense.id,
            user_id=uid,
            share_amount=share
        )
        db.add(split)

    db.commit()

    return new_expense
