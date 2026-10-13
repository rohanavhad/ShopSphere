from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.user import User
from app.schemas.order import OrderCreate

def create_order(db: Session, user: User, payload: OrderCreate) -> Order:
    # Aggregate repeated product IDs to avoid duplicate stock checks/items.
    quantities: dict[int, int] = {}
    for item in payload.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity

    products = {}
    for product_id, quantity in quantities.items():
        product = db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).with_for_update().first()
        if not product:
            raise ValueError(f"Product {product_id} does not exist or is unavailable")
        if product.stock < quantity:
            raise ValueError(f"Insufficient stock for '{product.name}'")
        products[product_id] = product

    total = sum((Decimal(str(products[pid].price)) * qty for pid, qty in quantities.items()), Decimal("0.00"))
    order = Order(user_id=user.id, status="pending", total_amount=total)
    db.add(order)
    db.flush()
    for product_id, quantity in quantities.items():
        product = products[product_id]
        product.stock -= quantity
        db.add(OrderItem(order_id=order.id, product_id=product_id, quantity=quantity,
                         unit_price=product.price))
    db.commit()
    return db.query(Order).options(joinedload(Order.items)).filter(Order.id == order.id).first()

def list_orders(db: Session, user: User):
    return db.query(Order).options(joinedload(Order.items)).filter(Order.user_id == user.id).order_by(Order.id.desc()).all()
