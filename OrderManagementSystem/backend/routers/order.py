from fastapi import APIRouter, Depends
from controllers import order
from schemas.order import OrderCreate
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.helper import require_role

order_route = APIRouter()

@order_route.post("/")
def create_order(body: OrderCreate, db:Session = Depends(get_db), current_user = Depends(require_role(["user"]))):
    return order.create_order(body, db, current_user)

@order_route.get("/all")
def get_all_orders(db:Session = Depends(get_db), current_user = Depends(require_role(["user"]))):
    return order.get_all_orders(db, current_user)

# vendor specific orders
@order_route.get("/user-orders")
def get_user_orders(db:Session = Depends(get_db), current_user = Depends(require_role(["vendor"]))):
    return order.get_user_orders(db, current_user)