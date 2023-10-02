from fastapi import FastAPI
from .routers import category, item

app = FastAPI()

app.include_router(category.router)
app.include_router(item.router)