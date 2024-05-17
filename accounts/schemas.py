from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    user_id: int
    name: str
    balance: float

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None

class Account(BaseModel):
    id: int
    user_id: int
    name: str
    balance: float
