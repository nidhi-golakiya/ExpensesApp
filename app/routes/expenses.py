# app/routes/expenses.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database, auth

router = APIRouter()

@router.post("/expenses")
def create_expense(exp: schemas.ExpenseCreate, db: Session = Depends(database.get_db),
                   user: models.User = Depends(auth.get_current_user)):
    new_exp = models.Expense(
        category = exp.category, 
        amount = exp.amount,
        user_id = user.id)
    db.add(new_exp)
    db.commit()
    db.refresh(new_exp)
    return {"message": "Expense created successfully"}

@router.get("/expenses")
def get_expenses(db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    expenses = db.query(models.Expense).filter(models.Expense.user_id == user.id).all()
    return expenses
