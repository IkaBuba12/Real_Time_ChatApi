from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ChatRoomCreate(BaseModel):
    name: str

class ChatRoomResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
