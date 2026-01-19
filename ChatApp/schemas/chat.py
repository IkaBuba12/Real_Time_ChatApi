from pydantic import BaseModel
from datetime import datetime

class ChatRoomCreate(BaseModel):
    name: str

class ChatRoomResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
