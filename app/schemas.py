from typing import List, Optional, Set
from pydantic import BaseModel, Field, HttpUrl, EmailStr


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    comments: Optional[List[str]] = []
    tags: Optional[Set[str]] = set()
    image: Optional[Image] = None


class State(BaseModel):
    uf: str
    name: str


class Address(BaseModel):
    street: str = Field(..., example='Rua X')
    number: int
    complement: Optional[str] = Field(None, example='Proximo a Praça X')
    district: str = Field(..., example='Dom Bosco')
    city: str
    state: State
    country: str


class User(BaseModel):
    username: str
    full_name: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'username': 'foo',
                'full_name': 'bar'
            }
        }


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


class Product(BaseModel):
    code: str
    price: float
    quantity: Optional[int]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class GetUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class ProgrammingLanguage(BaseModel):
    name: str
    category: str

    languages = {
        "ruby": {"name": "Ruby", "category": "Back-End"},
        "csharp": {"name": "C#", "category": "Back-End"}
    }
