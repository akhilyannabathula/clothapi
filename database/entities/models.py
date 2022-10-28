import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database.config.dbconfig import Base,engine


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    date = Column(Date,default=datetime.date.today())
    phone_number = Column(String)

    items = relationship("Items", back_populates="order")


class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, index=True)
    description = Column(String, index=True)
    date = Column(Date, default=datetime.date.today())
    order_id = Column(Integer, ForeignKey("orders.id"))
    sold_price = Column(Integer)
    source = Column(String)
    order = relationship("Orders", back_populates="items")



Base.metadata.create_all(engine)

