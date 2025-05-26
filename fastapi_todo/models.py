from sqlmodel import SQLModel, Field
from typing import Optional

class Student(SQlModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age : int
    grade: str
