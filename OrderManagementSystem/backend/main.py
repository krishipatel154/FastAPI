from fastapi import FastAPI
from routers import auth, vendor
from utils.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.auth_router, prefix="/user")
app.include_router(vendor.vendor_router, prefix="/vendor")

@app.get("/")
async def root():
    return {"message": "Order Management System"}