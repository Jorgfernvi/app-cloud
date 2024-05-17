from pydantic import BaseModel
from datetime import date
from typing import Optional

class LoanRequest(BaseModel):
    user_id: int
    amount: float
    term_months: int

class LoanStatusUpdate(BaseModel):
    loan_id: int
    status: str

class LoanPayment(BaseModel):
    loan_id: int
    amount: float
    payment_date: date

class Loan(BaseModel):
    id: int
    user_id: int
    amount: float
    balance: float
    term_months: int
    status: str
    created_at: date
