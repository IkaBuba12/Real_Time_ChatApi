from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ChatApp.schemas.schemas import UserCreate
from ChatApp.routers.chat import get_db
from ChatApp.services.auth_services import register_user, authenticate_user

router = APIRouter(
    prefix="",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return register_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        token = authenticate_user(db, form_data.username, form_data.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
