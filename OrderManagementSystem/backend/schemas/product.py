from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Literal, Optional
from decimal import Decimal

class CatgorySchema(BaseModel):
    name: Annotated[str, Field(title="Name of the product category", max_length=255)]

class CatgoryResponseSchema(BaseModel):
    id: int
    name: str

class ProductSchema(BaseModel):
    name: Annotated[str, Field(title="Name of the product", max_length=255)]
    image_url: Optional[HttpUrl] = None
    description: Annotated[Optional[str], Field(title="Description of the product", max_length=500)] = None
    price: Annotated[Decimal, Field(gt=0, le=100000)]
    quantity: Annotated[int, Field(ge=0, title="Quantity of the product")]
    category_id: int

class ProductUpdateSchema(BaseModel):
    name: Optional[Annotated[str, Field(max_length=255)]] = None
    image_url: Optional[HttpUrl] = None
    description: Optional[Annotated[str, Field(title="Description of the product", max_length=500)]] = None
    price: Optional[Annotated[Decimal, Field(gt=0, le=100000)]] = None
    quantity: Optional[Annotated[int, Field(ge=0)]] = None

class ProductResponse(ProductSchema):
    id: int
    stock_status: Literal["in_stock", "low_stock", "out_of_stock"]

    class Config:
        from_attributes = True  # for SQLAlchemy