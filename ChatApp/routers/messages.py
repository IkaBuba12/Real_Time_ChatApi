from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ChatApp.core.database import SessionLocal
from ChatApp.core.security import get_current_user
from ChatApp.schemas.message import MessageCreate
from ChatApp.services.chat_services import get_room_messages, send_message

router = APIRouter(prefix="/chatrooms", tags=["Messages"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{room_id}/messages")
def get_messages(
    room_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    print("Room ID:", room_id)
    messages = get_room_messages(db, room_id, limit)
    print("Messages:", messages)
    return messages


@router.post("/{room_id}/messages")
def post_message(
    room_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    message.room_id = room_id
    return send_message(db, message, current_user.id)

