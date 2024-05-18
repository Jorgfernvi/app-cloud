from pydantic import BaseModel

class Card(BaseModel):
    user_id: int
    card_number: str
    card_type: str
    balance: float

