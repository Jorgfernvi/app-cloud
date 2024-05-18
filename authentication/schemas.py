from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class TokenVerification(BaseModel):
    token: str

class ChangePassword(BaseModel):
    user_id: int
    old_password: str
    new_password: str

class RecoverPassword(BaseModel):
    email: str
