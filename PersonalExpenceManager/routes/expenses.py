from fastapi import APIRouter, Depends, Request
from controllers import expenses
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.helper import is_authenticated
from models.expenses import ExpensesModel

expenses_router = APIRouter()

@expenses_router.get("/")
def get_expenses(db: Session = Depends(get_db), user = Depends(is_authenticated)):
    return expenses.get_expenses(db, user)

@expenses_router.post("/")
def post_expenses(request: Request, body:ExpensesModel, db:Session = Depends(get_db), user = Depends(is_authenticated)):
    return expenses.post_expenses(request, body, db)

@expenses_router.get("/{id}")
def get_by_id(id: int, db:Session = Depends(get_db), user = Depends(is_authenticated)):
    return expenses.get_by_id(id, db, user)

@expenses_router.put("/{id}")
def update_expence(id: int,request: Request, body:ExpensesModel, db:Session = Depends(get_db), user = Depends(is_authenticated)):
    return expenses.update_expense(id,request, body, db)

@expenses_router.delete("/{id}")
def delete_expense(id: int,request: Request, db:Session = Depends(get_db), user = Depends(is_authenticated)):
    return expenses.delete_expense(id, request, db)