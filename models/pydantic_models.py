from typing import List

import pydantic
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    item_type : str
    description: str
    order_id: int

    class Config:
        orm_mode = True

class UpdateOrders(BaseModel):
    id: int
    customer_name: str
    class Config:
        orm_mode = True




class Orders(BaseModel):
    id: int
    customer_name : str
    items: List[Item] = []

    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    item_type : str
    description: str

    class Config:
        orm_mode = True


class OrdersCreate(BaseModel):
    customer_name : str
    items: List[ItemCreate] = []

    class Config:
        orm_mode = True