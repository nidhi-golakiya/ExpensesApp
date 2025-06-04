# app/routes/expenses.py
from fastapi import APIRouter, Depends, HTTPException, Query
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

@router.put("/expenses")
def update_expense(
    expense_id: int = Query(...),
    new_amount: float = Query(None),
    new_category: str = Query(None),
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if new_amount is not None:
        expense.amount = new_amount
    if new_category is not None:
        expense.category = new_category

    db.commit()
    return {"message": "Expense updated successfully"}


@router.delete("/expenses")
def delete_expense(
    expense_id: int = Query(...),
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}
