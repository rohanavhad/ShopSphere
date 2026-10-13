from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token

def register(db: Session, payload: RegisterRequest) -> tuple[User, str]:
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise ValueError("An account with this email already exists")
    user = User(email=payload.email.lower(), full_name=payload.full_name.strip(),
                hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, create_access_token(str(user.id))

def login(db: Session, payload: LoginRequest) -> tuple[User, str]:
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise ValueError("Incorrect email or password")
    if not user.is_active:
        raise ValueError("This account is inactive")
    return user, create_access_token(str(user.id))
