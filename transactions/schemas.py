from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float

class ServicePaymentRequest(BaseModel):
    account_id: int
    service_provider_id: int
    amount: float

class Transaction(BaseModel):
    id: int
    from_account: Optional[int] = None
    to_account: Optional[int] = None
    amount: float
    transaction_type: str
    timestamp: datetime
