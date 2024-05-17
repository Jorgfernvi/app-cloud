from pydantic import BaseModel
from datetime import date

class ReportRequest(BaseModel):
    user_id: int
    start_date: date
    end_date: date

class ExpenseReport(BaseModel):
    total_expenses: float
    categories: dict

class IncomeReport(BaseModel):
    total_income: float
    sources: dict
