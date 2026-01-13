from pydantic import BaseModel
from typing import List
from datetime import datetime


class ExpenseCreate(BaseModel):
    group_id: int
    amount: float
    description: str | None = None
    split_between: List[int]

class GroupNameOnly(BaseModel):
    name: str

    class Config:
        from_attributes = True

class ExpenseResponse(BaseModel):
    id: int
    group_id: int
    paid_by: int
    amount: float
    description: str | None
    created_at: datetime
    group: GroupNameOnly 

    class Config:
        from_attributes = True

