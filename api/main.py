from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import get_db
import jwt
import datetime

from fastapi.middleware.cors import CORSMiddleware
from models.accounts import AccountRouter

app = FastAPI()

SECRET_KEY ="your_secret_key"
ALGORITHM = "HS256"


origins = [
    "http://localhost:5173",  # Allow localhost for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # SessionMiddleware(secret_key="secret_key"),
)


class User(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(
    user: User,
    db = Depends(get_db)
    ):
    query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts WHERE Email = %s AND Password = %s"
    cursor = db[0].cursor()
    cursor.execute(query, (user.username, user.password))   
    account = cursor.fetchone()  
    if account:
        token_data = {
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")


app.include_router(AccountRouter, prefix="/api")
