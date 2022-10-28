from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class GarmentType(str, Enum):
    TSHIR = "tshirt"
    JEAN = "jean"
    SHIRT = "shirt"
    TROUSER = "trouser"
    SHORT = "short"
    HOODIE = "hoodie"
    OTHER = "other"


class GarmentSource(str, Enum):
    MYNTRA = "myntra"
    AJIO = "ajio"
    BANGLORE = "banglore"
    ONLINE = "online"


class Item(BaseModel):
    id: int
    item_type: GarmentType
    description: Optional[str] = None
    order_id: int
    sold_price: int
    source: Optional[GarmentSource] = GarmentSource.BANGLORE

    class Config:
        orm_mode = True


class UpdateOrders(BaseModel):
    id: int
    customer_name: str

    class Config:
        orm_mode = True


class Orders(BaseModel):
    id: int
    customer_name: str
    items: List[Item]

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    item_type: GarmentType
    description: Optional[str] = None
    sold_price: int
    source: Optional[GarmentSource] = GarmentSource.BANGLORE

    class Config:
        orm_mode = True


class OrdersCreate(BaseModel):
    customer_name: str
    items: List[ItemCreate]

    class Config:
        orm_mode = True
