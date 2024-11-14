from fastapi import FastAPI
from app.routes import logbook_crud, logbook_functions

app = FastAPI()

app.include_router(logbook_crud.router, prefix="/logbooks")
app.include_router(logbook_functions.router, prefix="/logbooks")

