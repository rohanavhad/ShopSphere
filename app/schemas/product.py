from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    image_url: str
    is_active: bool

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str = ""
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)
    image_url: str = ""
