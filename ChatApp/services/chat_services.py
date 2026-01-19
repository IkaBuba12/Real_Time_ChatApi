from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ChatApp.models.message import Message
from ChatApp.models.chatroom import ChatRoom
from ChatApp.schemas.message import MessageCreate
from ChatApp.schemas.chat import ChatRoomCreate


def create_message(
    db: Session,
    message_data: MessageCreate,
    sender_id: int
):

    room = (
        db.query(ChatRoom)
        .filter(ChatRoom.id == message_data.room_id)
        .first()
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )

    message = Message(
        content=message_data.content,
        room_id=message_data.room_id,
        sender_id=sender_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def create_chat_room(db: Session, data: ChatRoomCreate):
    existing = (
        db.query(ChatRoom)
        .filter(ChatRoom.name == data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat room already exists"
        )

    room = ChatRoom(name=data.name)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def list_chat_rooms(db: Session):
    return db.query(ChatRoom).all()


def send_message(
    db: Session,
    message_data: MessageCreate,
    sender_id: int
):
    room = (
        db.query(ChatRoom)
        .filter(ChatRoom.id == message_data.room_id)
        .first()
    )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat room not found"
        )

    message = Message(
        content=message_data.content,
        sender_id=sender_id,
        room_id=message_data.room_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_room_messages(db: Session, room_id: int, limit: int = 50):
    return (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )


def delete_message(db: Session, message_id: int, user_id: int):
    message = (
        db.query(Message)
        .filter(Message.id == message_id)
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    if message.sender_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this message"
        )

    db.delete(message)
    db.commit()
    return {"detail": "Message deleted"}
