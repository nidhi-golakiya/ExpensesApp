# app/main.py
from fastapi import FastAPI
from app.routes import expenses, users
from app import database
from app import models

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# Routes
app.include_router(expenses.router)
app.include_router(users.router)
