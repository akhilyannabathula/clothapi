import fastapi
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import pydantic_models
from database.crudrepo import order_repository
from database.config.dbconfig import SessionLocal,engine
from database.entities import models
from fastapi.responses import FileResponse



app = FastAPI(debug=True)


#models.Base.metadata.create_all(bind=engine)

#Dependency
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
def place_order(data: pydantic_models.OrdersCreate, db: Session = Depends(get_db)):
    return order_repository.create_order(db,data)

@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    return order_repository.get_orders(db)

@app.get("/recent_orders")
def get_recent_orders(db: Session = Depends(get_db)):
    return order_repository.get_recent_orders(db)

@app.get("/recent_items")
def get_recent_items(db: Session = Depends(get_db)):
    return order_repository.get_recent_items(db)


@app.get("/item/{id}")
def get_item_by_id( id: int,  db: Session = Depends(get_db)):
    return order_repository.get_item(db,id)

@app.get("/order/{id}")
def get_order_by_id( id: int,  db: Session = Depends(get_db)):
    return order_repository.get_order(db,id)

@app.put("/order_and_items")
def update_order_and_items(data: pydantic_models.Orders, db: Session = Depends(get_db)):
    return order_repository.update_order_and_items( db, data )

@app.put("/order")
def update_order(data: pydantic_models.UpdateOrders, db: Session = Depends(get_db)):
    return order_repository.update_order( db, data )

@app.put("/item")
def update_item(data: pydantic_models.Item, db: Session = Depends(get_db)):
    return order_repository.update_item( db, data )

@app.get("/download_db")
def download_database_file():
    path = 'clothe_store.db'
    return FileResponse(path=path,filename=path,media_type='application/octet-stream')



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
