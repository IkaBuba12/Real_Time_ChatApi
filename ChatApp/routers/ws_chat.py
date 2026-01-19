from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from ChatApp.models.message import Message
from ChatApp.core.connection_manager import manager, get_db

router = APIRouter(prefix="/ws", tags=["WebSocket Chat"])

@router.websocket("/chat/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            sender_id = data.get("sender_id")
            content = data.get("content")

            message = Message(content=content, sender_id=sender_id, room_id=room_id)
            db.add(message)
            db.commit()
            db.refresh(message)

            await manager.broadcast(room_id, {
                "id": message.id,
                "sender_id": message.sender_id,
                "room_id": message.room_id,
                "content": message.content,
                "created_at": str(message.created_at)
            })
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
