import json
import jwt
import datetime
from db import get_db
from typing import List
from pydantic import BaseModel
from jwt import PyJWTError, decode
from starlette.websockets import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, Form, Body


app = FastAPI()
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


manager = ConnectionManager()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(user: User, response: Response, db=Depends(get_db)):
    query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts WHERE Email = %s AND Password = %s"
    cursor = db[0].cursor()
    cursor.execute(query, (user.username, user.password))
    account = cursor.fetchone()

    if account:
        token_data = {
            "username": user.username,
            "account_id": account[1],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        response.set_cookie(
            key="access_token", value=token, httponly=True, samesite="none", secure=True
        )

        return {"message": "Logged in"}

    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    return token


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        accountid: str = payload.get("account_id")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "accountid": accountid}
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@app.get("/autheticate")
async def authenticate(token: str = Depends(oauth2_scheme)):
    if token:
        return {"message": "Authenticated"}
    else:
        raise HTTPException(status_code=401, detail="Unauthenticated")


@app.get("/all/users")
async def read_users(db=Depends(get_db)):
    query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts"
    cursor = db[0].cursor()
    cursor.execute(query)
    accounts = [{
                    "AccountTypeID": accounts[0],
                    "AccountID": accounts[1],
                    "FirstName": accounts[2],
                    "LastName": accounts[3],
                } for accounts in cursor.fetchall()
                ]
    return accounts


@app.post("/register")
async def create_user(
    Email: str = Body(...),
    FirstName: str = Body(...),
    LastName: str = Body(...),
    phone: str = Body(...),
    password: str = Body(...),
    db=Depends(get_db),
):

    query = "INSERT INTO accounts (FirstName, LastName, Password, Phone, Email) VALUES (%s, %s, %s, %s, %s)"
    cursor = db[0].cursor()
    cursor.execute(
        query, (FirstName, LastName, password, phone, Email)
    )

    cursor.execute("SELECT LAST_INSERT_ID()")
    cursor.fetchone()[0]
    cursor.execute("COMMIT")
    
    new_user = {
        "FirstName": FirstName,
        "LastName": LastName,
        "Password": password,
        "Phone": phone,
        "Email": Email,
    }

    await manager.broadcast(json.dumps(new_user))
    
    return new_user


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except Exception as e:
        print(e)
    finally:
        await manager.disconnect(websocket)
