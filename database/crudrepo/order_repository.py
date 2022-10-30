import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from models import pydantic_models
from database.entities import models


def create_order(db: Session, order: pydantic_models.OrdersCreate):
    db_order = models.Orders(customer_name=order.customer_name, phone_number=order.phone_number)
    for item in order.items:
        db_order.items.append(models.Items(**item.dict()))
    print(db_order)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Orders).options(joinedload('items')).offset(skip).limit(limit).all()


def get_items(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Items).options(joinedload('order')).offset(skip).limit(limit).all()


def get_recent_items(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Items).options(joinedload('order')).order_by(
        desc(models.Items.id)).offset(skip).limit(limit).all()


def get_recent_items_between(db: Session, from_date: datetime.date, to_date: datetime.date):
    return db.query(models.Items).filter(models.Items.date.between(from_date, to_date)).all()


def get_recent_orders_between(db: Session, from_date: datetime.date, to_date: datetime.date):
    return db.query(models.Orders).options(joinedload('items')).filter(
        models.Orders.date.between(from_date, to_date)).all()


def get_recent_orders(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Orders).options(joinedload('items')).order_by(
        desc(models.Orders.id)).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Orders).options(joinedload('items')).filter(models.Orders.id == order_id).first()


def get_item(db: Session, item_id: int):
    return db.query(models.Items).options(joinedload('order')).filter(models.Items.id == item_id).first()


def update_order_and_items(db: Session, order: pydantic_models.OrdersCreate):
    db_order = get_order(db, order_id=order.id)
    db_order.customer_name = order.customer_name
    db_order.phone_number = order.phone_number

    for item in order.items:
        update_item(db, item=item)

    db.commit()
    db.refresh(db_order)
    return db_order


def delete_item_by_id(db: Session, id: int):
    item = get_item(db=db, item_id=id)
    db.delete(item)
    db.commit()
    return item


def update_order(db: Session, order: pydantic_models.OrdersCreate):
    db_order = get_order(db, order.id)
    db_order.customer_name = order.customer_name
    db_order.phone_number = order.phone_number
    db.commit()
    db.refresh(db_order)
    return db_order


def update_item(db: Session, item: pydantic_models.Item):
    # db_item = models.Items( **item.dict() )
    # db.commit()
    # db.merge(db_item)
    # db.commit()
    # db.refresh(db_item)
    resp = db.query(models.Items).filter(models.Items.id == item.id).update(dict(item))
    db.commit()
    return item
