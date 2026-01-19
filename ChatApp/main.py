from fastapi import FastAPI
from ChatApp.routers import chat, messages, ws_chat, auth
from fastapi.responses import RedirectResponse
from ChatApp.core.database import Base, engine
app = FastAPI(title="Chat API")

app.include_router(chat.router)
app.include_router(messages.router)
app.include_router(ws_chat.router)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to ChatApp API!"}
@app.get("/")
def root_redirect():
    return RedirectResponse(url="/docs")

Base.metadata.create_all(bind=engine)
