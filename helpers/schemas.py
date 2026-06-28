from typing import Optional
from pydantic import BaseModel, field_validator


class ProductSchema(BaseModel):
    id: int
    title: str
    price: float
    cat: str
    desc: Optional[str] = None
    image: Optional[str] = None

    @field_validator("title", "cat")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        assert len(v) > 0, "Field must not be empty"
        return v

    @field_validator("price")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        assert v > 0, "Price must be positive"
        return v


class ProductListSchema(BaseModel):
    Items: list[ProductSchema]


class CartItemSchema(BaseModel):
    id: str
    cookie: str
    prod_id: int


class CartSchema(BaseModel):
    Items: Optional[list[CartItemSchema]] = None
