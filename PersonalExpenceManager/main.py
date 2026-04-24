from fastapi import FastAPI
from routes.user import user_router
from routes.expenses import expenses_router
from utils.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(expenses_router, prefix="/expenses")