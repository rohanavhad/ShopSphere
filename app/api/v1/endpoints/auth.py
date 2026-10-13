from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserOut
from app.services import auth_service
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user, token = auth_service.register(db, payload)
    return {"access_token": token, "user": user}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user, token = auth_service.login(db, payload)
    return {"access_token": token, "user": user}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
