import datetime
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Form, Cookie, Request

# from fastapi_sessions import Session
from db import get_db
from pydantic import BaseModel
import bcrypt
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer



AccountRouter = APIRouter()


class Login(BaseModel):
    email: str
    password: str


class AccountResponse(BaseModel):
    AccountTypeID: int = None
    AccountID: int = None
    FirstName: str = None
    LastName: str = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


# Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret key and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


# @AccountRouter.get("/accounts/", response_model=list)
# async def read_users(db=Depends(get_db)):
#     query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts"
#     db[0].execute(query)
#     accounts = [
#         {
#             "AccountTypeID": accounts[0],
#             "AccountID": accounts[1],
#             "FirstName": accounts[2],
#             "LastName": accounts[3],
#         }
#         for accounts in db[0].fetchall()
#     ]
#     return accounts


from fastapi import Cookie

# @AccountRouter.post("/accounts/login", response_model=AccountResponse)
# async def login_user(login: Login, db=Depends(get_db), session: Session = Depends(get_session)):
#     query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts WHERE Email = %s AND Password = %s"
#     try:
#         db[0].execute(query, (login.email, login.password))
#         account = db[0].fetchone()
#         if account is not None:
#             # Create session upon successful login
#             session["user_id"] = account[1]  # Assuming AccountID is used as the user identifier
#             return {
#                 "AccountTypeID": account[0],
#                 "AccountID": account[1],
#                 "FirstName": account[2],
#                 "LastName": account[3],
#             }
#         else:
#             raise HTTPException(status_code=404, detail="User not found")
#     except Exception as e:
#         print(e)


# @AccountRouter.post("/accounts/login", response_model=AccountResponse)
# async def login_user(
#     request: Request, form_data: OAuth2PasswordRequestForm = Depends()
# ):
#     db = get_db()
#     try:
#         cursor = db.cursor()
#         query = "SELECT AccountTypeID, AccountID, FirstName, LastName FROM accounts WHERE Email = %s AND Password = %s"
#         cursor.execute(query, (form_data.username, form_data.password))
#         user_data = cursor.fetchone()

#         if not user_data:
#             raise HTTPException(status_code=400, detail="Invalid Credentails")

#         request.session["email"] = form_data.username
#         return RedirectResponse(url="/welcome", status_code=302)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Database error") from e


@AccountRouter.post("/accounts/login", response_model=LoginResponse)
def login_user(login_request: Login):
    with get_db.cursor() as cursor:
        query = "SELECT * FROM accounts WHERE Email = %s"
        cursor.execute(query, (login_request.email,))
        user_data = cursor.fetchone()

        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")


# @AccountRouter.post("/accounts/logout")
# async def logout_user(session: Session = Depends(get_session)):
#     session.clear()  # Clear the session data
#     return {"message": "Logged out successfully"}
