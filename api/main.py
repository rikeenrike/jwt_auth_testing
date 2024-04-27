from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from db import get_db
import jwt
import datetime
from jwt import PyJWTError, decode
from fastapi.middleware.cors import CORSMiddleware
from models.accounts import AccountRouter

app = FastAPI()

SECRET_KEY ="your_secret_key"
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
async def login(
    user: User,
    response: Response,
    db = Depends(get_db)
    ):
    query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts WHERE Email = %s AND Password = %s"
    cursor = db[0].cursor()
    cursor.execute(query, (user.username, user.password))   
    account = cursor.fetchone()  
    if account:
        token_data = {
            "username": user.username,
            "account_id": account[1],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        response.set_cookie(key="access_token", value=token, httponly=True, samesite="none", secure=True)  
        
        return {"message": "Logged in"}
        
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

from fastapi import Request


def oauth2_scheme(request: Request):
    token = request.cookies.get("access_token")
    return token


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username}
    except PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
