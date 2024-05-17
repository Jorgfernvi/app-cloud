from pydantic import BaseModel
from datetime import date
from typing import Optional

class CardCreate(BaseModel):
    account_id: int
    card_number: str
    card_type: str
    expiration_date: date

class CardUpdate(BaseModel):
    card_number: Optional[str] = None
    card_type: Optional[str] = None
    expiration_date: Optional[date] = None

class Card(BaseModel):
    id: int
    account_id: int
    card_number: str
    card_type: str
    expiration_date: date

class CardBlockRequest(BaseModel):
    card_id: int
    blocked: bool

class CardTransaction(BaseModel):
    card_id: int
    amount: float
    timestamp: date
