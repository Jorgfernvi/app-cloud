from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int
    message: str

class Notification(BaseModel):
    id: int
    user_id: int
    message: str
    read: bool
