from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductOut, ProductCreate
from app.services import product_service

router = APIRouter()

@router.get("/", response_model=list[ProductOut])
def get_products(q: str | None = None, skip: int = Query(0, ge=0),
                 limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return product_service.list_products(db, q=q, skip=skip, limit=limit)

# Demo/admin endpoint: add authentication + role-based authorization before production use.
@router.post("/", response_model=ProductOut, status_code=201)
def add_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, payload)
