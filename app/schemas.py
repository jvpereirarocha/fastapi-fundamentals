from typing import Optional
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


class DeclaredItem(BaseModel):
    name: str = Field(..., title='Item name', min_length=3, max_length=200)
    description: Optional[str] = Field(
        None, title='The item description', max_length=300
    )
    price: float = Field(
        ...,
        gt=0,
        description='The price of the item must be greather than zero'
    )
    tax: float = Field(None, title='The item tax')
