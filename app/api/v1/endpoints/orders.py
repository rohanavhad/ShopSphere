from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import create_order, list_orders

router = APIRouter()

@router.post("/", response_model=OrderOut, status_code=201)
def place_order(payload: OrderCreate, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    return create_order(db, user, payload)

@router.get("/", response_model=list[OrderOut])
def my_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list_orders(db, user)
