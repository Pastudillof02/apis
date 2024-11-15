from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from pydantic import EmailStr
from app.models.usuario import Usuario
from app.routes.usuario_crud import get_user
from app.db import usuarios

router = APIRouter()

@router.get("/{id}/contactos")
def get_contactos(id: str):
    contactos = []

    try:
        usuario = usuarios.find_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for c in usuario.get("contactos", []):
        contact = usuarios.find_one({"email": c})

        if contact is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with email {c} not found")

        contactos.append(contact["email"])
        
    return jsonable_encoder(contactos)


@router.post("/{id}/contactos")
def add_contacto(id: str, email: EmailStr):
    try:
        usuario = usuarios.find_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if usuarios.find_one({"email": email}) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with email {email} not found")

    if email in usuario.get("contactos", []):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Contact with email {email} already exists")

    usuario["contactos"].append(email)

    usuarios.update_one({"_id": ObjectId(id)}, {"$set": usuario})

    return {"message": f"Contact with email {email} added to user with ID {id}"}


@router.delete("/{id}/contactos")
def delete_contacto(id: str, email: EmailStr):
    try:
        usuario = usuarios.find_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if email not in usuario.get("contactos", []):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with email {email} not found")

    usuario["contactos"].remove(email)

    usuarios.update_one({"_id": ObjectId(id)}, {"$set": usuario})

    return {"message": f"Contact with email {email} removed from user with ID {id}"}