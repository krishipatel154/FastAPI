from pydantic import BaseModel

# data validation
class TaskSchema(BaseModel):
    title: str
    description: str
    is_completed: bool = False

class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool