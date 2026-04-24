from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime

class CategoriesModel(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name of the category")]

class ExpensesModel(BaseModel):
    amount: Annotated[float, Field(default=0, title="Amount of the expence")]
    description: Annotated[Optional[str], Field(title="Description of expence")]
    date: Annotated[datetime, Field(title="Date and time of the expence")]
    category: Annotated[str, Field(title="Category name")]
    