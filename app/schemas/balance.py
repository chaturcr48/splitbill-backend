from pydantic import BaseModel

class BalanceResponse(BaseModel):
    from_user: int
    to_user: int
    amount: float
