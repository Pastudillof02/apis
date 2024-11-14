from fastapi import FastAPI
from app.routes import geocache_crud, geocache_functions, geocache_logbook

app = FastAPI()

app.include_router(geocache_crud.router, prefix="/geocaches")
app.include_router(geocache_functions.router, prefix="/geocaches") 
app.include_router(geocache_logbook.router, prefix="/geocaches")

