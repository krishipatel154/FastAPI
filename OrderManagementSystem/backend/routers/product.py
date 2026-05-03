from fastapi import APIRouter, Depends
from controllers import product
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.helper import require_role
from schemas.product import ProductSchema, CatgorySchema, ProductUpdateSchema

product_route = APIRouter()

# product category apis
@product_route.post("/category")
def add_category(body:CatgorySchema, db:Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    return product.add_category(body, db, current_user)

@product_route.get("/category")
def get_category(db:Session = Depends(get_db), current_user = Depends(require_role(["user", "vendor"]))):
    return product.get_category(db, current_user)

@product_route.post("/")
def add_product(body:ProductSchema, db:Session = Depends(get_db), current_user = Depends(require_role(["vendor"]))):
    return product.add_product(body, db, current_user)

# get product for vendor
@product_route.get("/")
def get_product(db: Session = Depends(get_db), current_user = Depends(require_role(["vendor"]))):
    return product.get_product(db, current_user)

@product_route.get("/all-products")
def get_all_product(db: Session = Depends(get_db), current_user = Depends(require_role(["user"]))):
    return product.get_all_product(db, current_user)

@product_route.patch("/")
def update_product(id:int, body:ProductUpdateSchema, db:Session = Depends(get_db), current_user = Depends(require_role(["vendor"]))):
    return product.update_product(id, body, db, current_user)

@product_route.delete("/")
def delete_product(id:int, db:Session = Depends(get_db), current_user = Depends(require_role(["vendor"]))):
    return product.delete_product(id, db, current_user)