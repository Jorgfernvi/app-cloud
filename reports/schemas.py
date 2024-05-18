from pydantic import BaseModel
from typing import Optional

class Transaction(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    category: Optional[str] = None
