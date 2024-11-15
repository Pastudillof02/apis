import datetime
from typing import Tuple
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from pydantic import EmailStr
from app.routes.usuario_crud import get_user
from app.db import usuarios, eventos

router = APIRouter()

@router.get("/usuarios/{email}/contactos/getByName")
def get_contactos_by_name(email: EmailStr, name: str):
    contactos = []

    usuario = usuarios.find_one({"email": email})

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    regex = { "$regex": f".*{name}.*", "$options": "i" }

    for c in usuario["contactos"]:
        contacto = usuarios.find_one({"email": c, "nombre": regex})
        if contacto is not None:
            contacto["_id"] = str(contacto["_id"])
            contactos.append(contacto)
        
    return jsonable_encoder(contactos)


@router.put("/eventos/{id}/invitar")
def put_invitados(id: str, email: EmailStr):
    evento = eventos.find_one({"_id": ObjectId(id)})

    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    if email in evento["invitados"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already invited")
    
    evento["invitados"].append((email, "PENDIENTE"))

    try:
        eventos.update_one({"_id": ObjectId(id)}, {"$set": evento})
        return {"message": "Event updated"}
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    

@router.put("/eventos/{id}/confirmar")
def put_confirmar(id: str, email: EmailStr):
    evento = eventos.find_one({"_id": ObjectId(id)})

    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    for invitado in evento["invitados"]:
        if email in invitado:
            invitado[1] = "CONFIRMADO"

            try:
                eventos.update_one({"_id": ObjectId(id)}, {"$set": evento})
                return {"message": "Event updated"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not invited to event")


@router.put("/eventos/{id}/aplazar")
def put_aplazar(id: str, date: datetime.date):
    evento = eventos.find_one({"_id": ObjectId(id)})

    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    prev_date = evento["inicio"]
    prev_date = datetime.datetime.strptime(prev_date, "%Y-%m-%d").date()

    evento["inicio"] = date.strftime("%Y-%m-%d")

    diferencia = date - prev_date

    try:
        eventos.update_one({"_id": ObjectId(id)}, {"$set": evento})
        return {"message": f"Event postponed {diferencia.days} days"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    

@router.get("/agenda/getByEmail")
def get_agenda(email: EmailStr):
    eventos_list = []

    for e in eventos.find({"anfitrion": email}):
        e["_id"] = str(e["_id"])
        eventos_list.append(e)

    for e in eventos.find({"invitados": {"$elemMatch": {"$eq": email}} }):  
        e["_id"] = str(e["_id"])
        eventos_list.append(e)

    eventos_ordenados = sorted(eventos_list, key=lambda evento: evento["inicio"])
    
    return jsonable_encoder(eventos_ordenados)
