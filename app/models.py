from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# DB models for the to-do list app

# Create categories for the list items
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
        __tablename__ = "categories"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, unique=True, index=True)
        description = Column(String, index=True)
        is_active = Column(Boolean, default=True)
        created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
        
    # Create items for this list, attached to a category
class Item(Base):
        __tablename__ = "items"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, unique=True, index=True)
        description = Column(String, index=True)
        is_active = Column(Boolean, default=True)
        created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
        due_date = Column(TIMESTAMP)
        category_id = Column(Integer, ForeignKey("categories.id"))        
