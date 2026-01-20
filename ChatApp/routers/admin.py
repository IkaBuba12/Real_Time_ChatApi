from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ChatApp.core.database import SessionLocal
from ChatApp.models.models import User
from ChatApp.models.message import Message
from ChatApp.core.security import admin_only

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", dependencies=[Depends(admin_only)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/users/{user_id}", dependencies=[Depends(admin_only)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@router.get("/messages", dependencies=[Depends(admin_only)])
def all_messages(db: Session = Depends(get_db)):
    return db.query(Message).order_by(Message.created_at.desc()).all()


@router.get("/chatrooms/{room_id}/messages", dependencies=[Depends(admin_only)])
def room_messages(room_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(Message.created_at.desc())
        .all()
    )

