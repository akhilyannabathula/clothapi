from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.config.dbconfig import Base,engine


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)

    items = relationship("Items", back_populates="order")


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String, index=True)
    description = Column(String, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Orders", back_populates="items")


#Base.metadata.create_all(engine)

