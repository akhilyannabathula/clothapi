import fastapi
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from models import pydantic_models
from database.crudrepo import order_repository
from database.config.dbconfig import SessionLocal,engine
from database.entities import models
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#models.Base.metadata.create_all(bind=engine)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()










# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "akhil": {
        "username": "akhil",
        "full_name": "akhil",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class AuthUser(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme = HTTPBearer()



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    #to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(auth_user: AuthUser):
    user = authenticate_user(fake_users_db, auth_user.username, auth_user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}





@app.get("/health")
def read_root():
    return {"status": "UP"}


@app.post("/orders")
def place_order(data: pydantic_models.OrdersCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.create_order(db, data)

@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.get_orders(db)

@app.get("/recent_orders")
def get_recent_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user) ):
    return order_repository.get_recent_orders(db)

@app.get("/recent_items")
def get_recent_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.get_recent_items(db)


@app.get("/item/{id}")
def get_item_by_id( id: int,  db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.get_item(db,id)

@app.get("/order/{id}")
def get_order_by_id( id: int,  db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.get_order(db,id)

@app.put("/order_and_items")
def update_order_and_items(data: pydantic_models.Orders, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.update_order_and_items( db, data )

@app.put("/order")
def update_order(data: pydantic_models.UpdateOrders, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.update_order( db, data )

@app.put("/item")
def update_item(data: pydantic_models.Item, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return order_repository.update_item( db, data )

@app.get("/download_db")
def download_database_file(current_user: User = Depends(get_current_active_user)):
    path = 'clothe_store.db'
    return FileResponse(path=path,filename=path,media_type='application/octet-stream')



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
