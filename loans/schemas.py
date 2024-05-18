from typing import Optional
from pydantic import BaseModel


class LoanApplication(BaseModel):
    user_id: int
    amount: float
    term: int


class LoanStatusUpdate(BaseModel):
    status: str
