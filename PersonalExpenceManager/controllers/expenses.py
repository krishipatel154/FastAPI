from fastapi import HTTPException, Request, Response
from sqlalchemy.orm import Session
from schemas.expenses import ExpenseSchema, CategoriesSchema
from models.expenses import ExpensesModel
from utils.helper import current_user

def get_expenses(db: Session, user):
    try:
        # user_id = current_user(request)
        expenses = db.query(ExpenseSchema).filter(ExpenseSchema.user_id == user.id).all()
        if not expenses:
            return Response(content="Expence not found", status_code=404)
        return expenses

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def post_expenses(request: Request ,body:ExpensesModel, db:Session):
    try:
        user_id = current_user(request)
        category = body.category
        category_id = db.query(CategoriesSchema).filter(CategoriesSchema.name == category).first().id

        expense = ExpenseSchema(amount=body.amount, description = body.description, date=body.date, user_id = user_id, category_id = category_id)
        db.add(expense)
        db.commit()
        db.refresh(expense)

        return expense

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_by_id(id: int, db : Session, user):
    try:
        expense = db.query(ExpenseSchema).filter(ExpenseSchema.id == id).filter(ExpenseSchema.user_id == user.id).first()
        if not expense:
            return Response(content="Expence not found", status_code=404)
        return expense

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_expense(id:int,request:Request, body:ExpensesModel, db:Session):
    try:
        user_id = current_user(request)
        print(user_id)
        expense = db.query(ExpenseSchema).filter(ExpenseSchema.id == id).filter(ExpenseSchema.user_id == user_id).first()
        print(expense.user_id)
        if not expense:
            return Response(content="Expense not found", status_code=404)
        
        # user_id = current_user(request)
        category  = db.query(CategoriesSchema).filter(CategoriesSchema.name == body.category).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        expense.amount = body.amount
        expense.description = body.description
        expense.date = body.date
        expense.user_id = user_id
        expense.category_id = category.id
        
        # for key, value in body.dict().items():
        #     setattr(is_expense, key, value)

        db.commit()
        db.refresh(expense)

        return expense

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_expense(id:int, request: Request, db:Session):
    try:
        user_id = current_user(request)
        expense = db.query(ExpenseSchema).filter(ExpenseSchema.id == id).filter(ExpenseSchema.user_id == user_id).first()
        if not expense:
            return Response(content="Expense not found", status_code=404)
        
        db.delete(expense)
        db.commit()

        return Response(content="Expense deleted successfully", status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))