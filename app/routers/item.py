from typing import List
from .. import models
from .. import database
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas

# this router will handle CRUD for the to-do list items in the database

router = APIRouter(
    prefix="/item",
    tags=['Items']
)

# add an item

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
def create_item(request: schemas.Item, db: Session = Depends(database.get_db)):
    new_item = models.Item(name=request.name, description=request.description, due_date=request.due_date, category_id=request.category_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# get all items

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_all_items(db: Session = Depends(database.get_db)):
    items = db.query(models.Item).all()
    return items

# get a single item

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Item)
def get_single_item(id: int, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
    return item

# update an item

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_item(id: int, request: schemas.Item, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.id == id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
    item.update(request)
    db.commit()
    return item

# delete an item

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.id == id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
    item.delete(synchronize_session=False)
    db.commit()
    return "deleted"

# list all items in a category

@router.get('/{id}/items', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_items_in_category(id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).filter(models.Item.category_id == id).all()
    return items

# list all items in a category that are due today

@router.get('/{id}/items/today', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_items_in_category_due_today(id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).filter(models.Item.category_id == id).filter(models.Item.due_date == 'today').all()
    return items

# list all items in a category that are due tomorrow

@router.get('/{id}/items/tomorrow', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_items_in_category_due_tomorrow(id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).filter(models.Item.category_id == id).filter(models.Item.due_date == 'tomorrow').all()
    return items

# list all items in a category that are due this week

@router.get('/{id}/items/this-week', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_items_in_category_due_this_week(id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).filter(models.Item.category_id == id).filter(models.Item.due_date == 'this-week').all()
    return items

# list all items in a category that are due next week

@router.get('/{id}/items/next-week', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])

def get_items_in_category_due_next_week(id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).filter(models.Item.category_id == id).filter(models.Item.due_date == 'next-week').all()
    return items

# list all items in a category that are due this month

@router.get('/{id}/items/this-month', status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_items_in_category_due_this_month(id: int, db: Session = Depends(database.get_db)):
    items = db.query(models.Item).filter(models.Item.category_id == id).filter(models.Item.due_date == 'this-month').all()
    return items
