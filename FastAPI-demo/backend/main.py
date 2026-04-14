from fastapi import FastAPI, Depends
from database import SessionLocal,engine 
import schema
from sqlalchemy.orm import Session

app = FastAPI()

schema.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.get("/")
def hello():
    return "Hello"

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(schema.Product).all()
    return products

@app.get("/products/{id}")
def get_product(id:int, db: Session = Depends(get_db)):
    try:
        product = db.query(schema.Product).filter(id=id)
        return product
    
    except Exception as e:
        return "error"