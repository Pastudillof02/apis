from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from app.db import usuarios, eventos
from app.models.usuario import Usuario
from app.models.evento import Evento

router = APIRouter()

@router.get("")
def get_eventos():

    eventos_list = []

    for e in eventos.find():  
        e["_id"] = str(e["_id"])
        eventos_list.append(e)
        
    return jsonable_encoder(eventos_list)


@router.get("/getById")
def get_eventos(id: str):

    try:
        evento = eventos.find_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    evento["_id"] = str(evento["_id"])
        
    return jsonable_encoder(evento)


@router.post("")
def create_evento(evento: Evento):
    if not usuarios.find_one({"email": evento.anfitrion}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    for c in evento.invitados:
        if not usuarios.find_one({"email": c}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact not found")
    
    final_evento = jsonable_encoder(evento)
    evento_id = eventos.insert_one(final_evento).inserted_id

    return {"message": "Event created", "_id": str(evento_id)}

@router.put("")
def update_evento(id: str, evento: Evento):
    if not eventos.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event not found")
    
    if not usuarios.find_one({"email": evento.anfitrion}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    for c in evento.invitados:
        if not usuarios.find_one({"email": c}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact not found")
    
    try:
        eventos.update_one({"_id": ObjectId(id)}, {"$set": jsonable_encoder(evento)})
        return {"message": "Event updated"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    

@router.delete("")
def delete_evento(id: str):
    try:
        evento = eventos.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    eventos.delete_one({"_id": ObjectId(id)})

    return {"message": "Event deleted"}
