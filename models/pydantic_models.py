from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class GarmentType(str, Enum):
    TSHIR = "tshirt"
    JEAN = "jean"
    SHIRT = "shirt"
    HOODIE = "hoodie"
    UNDERWEAR = "underwear"
    COLLAR_TSHIR = "collar-tshirt"
    SWEAT_SHIRT = "sweatshirt"
    OTHER = "other"




class GarmentSource(str, Enum):
    MYNTRA = "myntra"
    AJIO = "ajio"
    BANGLORE = "banglore"
    ONLINE = "online"
    OTHER = "other"


class Item(BaseModel):
    id: int
    item_type: GarmentType
    description: Optional[str] = None
    order_id: int
    sold_price: int
    actual_price: int = 0
    brand: Optional[str] = None
    size: Optional[str] = None
    source: Optional[GarmentSource] = GarmentSource.BANGLORE

    class Config:
        orm_mode = True


class UpdateOrders(BaseModel):
    id: int
    customer_name: str
    phone_number: str

    class Config:
        orm_mode = True


class Orders(BaseModel):
    id: int
    customer_name: str
    items: List[Item]
    phone_number: str

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    item_type: GarmentType
    description: Optional[str] = None
    sold_price: int
    actual_price: int = 0
    brand: Optional[str] = None
    source: Optional[GarmentSource] = GarmentSource.BANGLORE
    size: Optional[str] = 'S'

    class Config:
        orm_mode = True


class OrdersCreate(BaseModel):
    customer_name: str
    items: List[ItemCreate]
    phone_number: str

    class Config:
        orm_mode = True

class ItemOut(BaseModel):
    id: int
    item_type: GarmentType
    description: Optional[str] = None
    order_id: int
    sold_price: int
    size: Optional[str] = None
    source: Optional[GarmentSource] = GarmentSource.BANGLORE

    class Config:
        orm_mode = True

class OrdersOut(BaseModel):
    id: int
    customer_name: str
    items: List[ItemOut]
    phone_number: str

    class Config:
        orm_mode = True


