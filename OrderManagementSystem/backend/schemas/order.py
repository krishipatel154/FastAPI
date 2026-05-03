from pydantic import BaseModel, Field
from typing import Annotated

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]
    shipping_address: str