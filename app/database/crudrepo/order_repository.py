from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from app.models import pydantic_models
from app.database.entities import models

def create_order(db: Session, order : pydantic_models.OrdersCreate):
    db_order = models.Orders( customer_name = order.customer_name)
    for item in order.items:
        db_order.items.append( models.Items(**item.dict()) )
    print(db_order)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Orders).options( joinedload('items') ).offset(skip).limit(limit).all()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Items).options( joinedload('order') ).offset(skip).limit(limit).all()


def get_recent_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Items).options( joinedload('order') ).order_by(
    desc(models.Items.id)).offset(skip).limit(limit).all()

def get_recent_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Orders).options( joinedload('items') ).order_by(
    desc(models.Orders.id) ).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Orders).options(joinedload('items')).filter(models.Orders.id == order_id).first()

def get_item(db: Session, item_id: int):
    return db.query(models.Items).options(joinedload('orders')).filter(models.Items.id == item_id).first()

def update_order_and_items(db: Session, order : pydantic_models.OrdersCreate):

    db_order = get_order(db, order_id = order.id)
    db_order.customer_name = order.customer_name

    for item in order.items:
        update_item(db,item=item)



    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order : pydantic_models.OrdersCreate):
    db_order = get_order(db, order.id)
    db_order.customer_name = order.customer_name
    db.commit()
    db.refresh(db_order)
    return db_order


def update_item(db: Session, item : pydantic_models.Item):
    # db_item = models.Items( **item.dict() )
    # db.commit()
    # db.merge(db_item)
    # db.commit()
    # db.refresh(db_item)
    resp = db.query(models.Items).filter( models.Items.id == item.id ).update( dict(item) )
    db.commit()
    return resp


