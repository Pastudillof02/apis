from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi import status
from app.db import usuarios
from app.models.usuario import Usuario

router = APIRouter()

@router.get("")
def get_users():
    usuarios_list = []

    for u in usuarios.find():

        u["_id"] = str(u["_id"])

        usuarios_list.append(u)
        
    return jsonable_encoder(usuarios_list)


@router.get("/getById")
def get_user(id: str):
    try:
        user = usuarios.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user["_id"] = str(user["_id"])

    return jsonable_encoder(user)


@router.post("")
def create_user(user: Usuario):
    if usuarios.find_one({"email": user.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    for c in user.contactos:
        if not usuarios.find_one({"email": c}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact not found")

    final_user = jsonable_encoder(user)
    user_id = usuarios.insert_one(final_user).inserted_id

    return {"message": "User created", "_id": str(user_id)}


@router.delete("")
def delete_user(id: str):
    try:
        user = usuarios.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    usuarios.delete_one({"_id": ObjectId(id)})

    return {"message": "User deleted"}

@router.put("")
async def update_user(id: str, user: Usuario):

    try:
        existing_user = usuarios.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    for c in user.contactos:
        contacto = usuarios.find_one({"email": c})
        if contacto is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Contacto {c} no encontrado")
    
    user_data = jsonable_encoder(user)
    
    try:
        usuarios.update_one(
            {"_id": ObjectId(id)},
            {"$set": user_data}
        )

        return {"message": "Usuario actualizado"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar usuario")

