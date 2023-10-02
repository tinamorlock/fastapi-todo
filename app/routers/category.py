from typing import List
from .. import models
from .. import database
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas

# this router will handle CRUD for the category section of the database

router = APIRouter(
    prefix="/category",
    tags=['Categories']
)

# add a category

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Category)
def create_category(request: schemas.Category, db: Session = Depends(database.get_db)):
    new_category = models.Category(name=request.name, description=request.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# get all categories

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Category])
def get_all_categories(db: Session = Depends(database.get_db)):
    categories = db.query(models.Category).all()
    return categories

# get a single category

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Category)
def get_single_category(id: int, db: Session = Depends(database.get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {id} not found")
    return category

# update a category

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_category(id: int, request: schemas.Category, db: Session = Depends(database.get_db)):
    category = db.query(models.Category).filter(models.Category.id == id)
    if not category.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {id} not found")
    category.update(request)
    db.commit()
    return "updated"

# delete a category

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)

def delete_category(id: int, db: Session = Depends(database.get_db)):
    category = db.query(models.Category).filter(models.Category.id == id)
    if not category.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {id} not found")
    category.delete(synchronize_session=False)
    db.commit()
    return "deleted"