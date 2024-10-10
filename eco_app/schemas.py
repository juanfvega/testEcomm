from pydantic import BaseModel
from enum import Enum

# Cart
class CartBase(BaseModel):
    pass

class CartCreate(CartBase):
    pass

class Cart(CartCreate):
    id: int 
    user_id:int 

    class Config:
        orm_mode = True

# User
class UserBase(BaseModel):
    email: str 

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int 
    is_active: bool
    carts: list[Cart] = []
    
    class Config:
        orm_mode = True
