from fastapi import FastAPI
from app.routes import tareas_crud, colaboradores_crud, advanced_functions

app = FastAPI()

app.include_router(tareas_crud.router, prefix="/tareas")
app.include_router(colaboradores_crud.router, prefix="/colaboradores")
app.include_router(advanced_functions.router, prefix="")



