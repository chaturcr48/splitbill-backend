from pydantic import BaseModel
from typing import List

class ExpenseCreate(BaseModel):
    group_id: int
    amount: float
    description: str | None = None
    split_between: List[int]

class ExpenseResponse(BaseModel):
    id: int
    group_id: int
    paid_by: int
    amount: float
    description: str | None
    group_name: str

    class Config:
        from_attributes = True


# # Updated Expense Schema for backend
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime

# class UserResponse(BaseModel):
#     id: int
#     name: str
#     email: str

# class GroupResponse(BaseModel):
#     id: int
#     name: str
#     description: Optional[str] = None

# class ExpenseResponse(BaseModel):
#     id: int
#     description: str
#     amount: float
#     paid_by: UserResponse
#     group: GroupResponse
#     split_between: List[UserResponse]
#     created_at: datetime

# class ExpenseCreate(BaseModel):
#     description: str
#     amount: float
#     group_id: int
#     split_between: List[int]
