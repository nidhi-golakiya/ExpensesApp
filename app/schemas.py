# app/schemas.py
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    message: str

class ExpenseCreate(BaseModel):
    category: str
    amount: float

