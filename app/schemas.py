import datetime
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str = None

class Category(CategoryBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    name: str
    description: str = None
    due_date: datetime.datetime = None
    category_id: int

class Item(ItemBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True