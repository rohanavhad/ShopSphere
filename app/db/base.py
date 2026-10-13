from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models so SQLAlchemy registers their metadata.
def load_models():
    from app.models import user, product, order  # noqa: F401
