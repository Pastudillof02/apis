from fastapi import FastAPI
from app.routes import usuario_crud, contacto_crud, evento_crud, advanced_functions

app = FastAPI()

app.include_router(usuario_crud.router, prefix="/usuarios")
app.include_router(contacto_crud.router, prefix="/usuarios")
app.include_router(evento_crud.router, prefix="/eventos")
app.include_router(advanced_functions.router, prefix="")

