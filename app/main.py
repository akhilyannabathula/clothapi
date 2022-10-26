from typing import Union

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import pydantic_models
from app.database.crudrepo import order_repository
from app.database.config.dbconfig import SessionLocal,engine
from app.database.entities import models



app = FastAPI()


#models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def read_root():
    return {"status": "UP"}


@app.post("/orders")
def make_purchase(data: pydantic_models.OrdersCreate,  db: Session = Depends(get_db)):
    return order_repository.create_order(db,data)

@app.get("/orders")
def make_purchase(db: Session = Depends(get_db)):
    return order_repository.get_orders(db)

@app.get("/recent_orders")
def make_purchase(db: Session = Depends(get_db)):
    return order_repository.get_recent_orders(db)

@app.get("/recent_items")
def make_purchase(db: Session = Depends(get_db)):
    return order_repository.get_recent_items(db)


@app.get("/item/{id}")
def make_purchase( id: int,  db: Session = Depends(get_db)):
    return order_repository.get_item(db,id)

@app.get("/order/{id}")
def make_purchase( id: int,  db: Session = Depends(get_db)):
    return order_repository.get_order(db,id)

@app.put("/order_and_items")
def update_purchase( data: pydantic_models.Orders ,  db: Session = Depends(get_db) ):
    return order_repository.update_order_and_items( db, data )

@app.put("/order")
def update_purchase( data: pydantic_models.UpdateOrders ,  db: Session = Depends(get_db) ):
    return order_repository.update_order( db, data )

@app.put("/item")
def update_purchase( data: pydantic_models.Item ,  db: Session = Depends(get_db) ):
    return order_repository.update_item( db, data )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
