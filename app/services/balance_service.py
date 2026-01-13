from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit

def calculate_group_balances(group_id: int, db: Session):
    balances = defaultdict(float)

    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    for expense in expenses:
        splits = (
            db.query(ExpenseSplit)
            .filter(ExpenseSplit.expense_id == expense.id)
            .all()
        )

        for split in splits:
            if split.user_id != expense.paid_by:
                key = (split.user_id, expense.paid_by)
                balances[key] += float(split.share_amount)

    result = []
    for (from_user, to_user), amount in balances.items():
        result.append({
            "from_user": from_user,
            "to_user": to_user,
            "amount": round(amount, 2)
        })

    return result
