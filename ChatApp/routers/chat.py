from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ChatApp.core.security import get_current_user
from ChatApp.core.database import get_db
from ChatApp.schemas.chat import ChatRoomCreate, ChatRoomResponse
from ChatApp.services.chat_services import create_chat_room, list_chat_rooms

router = APIRouter(
    prefix="/chatrooms",
    tags=["ChatRooms"]
)

@router.post(
    "/",
    response_model=ChatRoomResponse,
    status_code=201,
    operation_id="create_chatroom"
)
def create_room(
    data: ChatRoomCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_chat_room(db, data)

@router.get(
    "/",
    response_model=List[ChatRoomResponse],
    operation_id="list_chatrooms"
)
def get_rooms(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return list_chat_rooms(db)
