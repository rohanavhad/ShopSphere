from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def list_products(db: Session, q: str | None = None, skip: int = 0, limit: int = 20):
    query = db.query(Product).filter(Product.is_active.is_(True))
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    return query.order_by(Product.id.desc()).offset(skip).limit(limit).all()

def create_product(db: Session, payload: ProductCreate):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
