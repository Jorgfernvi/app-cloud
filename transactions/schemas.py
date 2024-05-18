from pydantic import BaseModel

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float

class Transaction(BaseModel):
    id: int
    from_account: int
    to_account: int
    amount: float
    transaction_type: str

