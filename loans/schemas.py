from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class Token(BaseModel):
    user_id: int
    token: str

class LoanApplication(BaseModel):
    user_id: int
    amount: float
    term: int

class LoanPayment(BaseModel):
    amount: float
