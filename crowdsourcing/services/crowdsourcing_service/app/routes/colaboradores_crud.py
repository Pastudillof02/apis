from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from fastapi.responses import JSONResponse
from app.db import colaboradores
from app.models.colaborador import Colaborador

router = APIRouter()

@router.get("")
def get_colaboradores():
    colaboradores_list = []

    for colaborador in colaboradores.find():
        colaborador["_id"] = str(colaborador["_id"])
        colaboradores_list.append(colaborador)

    return jsonable_encoder(colaboradores_list)

@router.get("/{id}")
def get_colaborador(id: str):
    try:
        colaborador = colaboradores.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if colaborador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    colaborador["_id"] = str(colaborador["_id"])

    return jsonable_encoder(colaborador)


@router.post("")
def create_colaborador(colaborador: Colaborador):
    if colaboradores.find_one({"email": colaborador.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El colaborador ya existe")
    
    colaborador_data = jsonable_encoder(colaborador)

    new_colaborador = colaboradores.insert_one(colaborador_data)
    created_colaborador = colaboradores.find_one({"_id": new_colaborador.inserted_id})

    if created_colaborador is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear el colaborador")
    
    created_colaborador["_id"] = str(created_colaborador["_id"])

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_colaborador)


@router.delete("/{id}")
def delete_colaborador(id: str):
    try:
        result = colaboradores.delete_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    return {"message": "Colaborador eliminado correctamente"}


@router.get("/{id}/habilidades")
def get_habilidades(id: str):
    try:
        colaborador = colaboradores.find_one({"_id": ObjectId(id)})
        if colaborador is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
        return jsonable_encoder(colaborador.get("habilidades", []))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")


@router.post("/{id}/habilidades")
def add_habilidad(id: str, habilidad: str):
    try:
        result = colaboradores.update_one(
            {"_id": ObjectId(id)},
            {"$addToSet": {"habilidades": habilidad}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
        
        return {"message": f"Habilidad '{habilidad}' añadida correctamente"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    
@router.delete("/{id}/habilidades")
def delete_habilidad(id: str, habilidad: str):
    try:
        result = colaboradores.update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"habilidades": habilidad}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador o habilidad no encontrada")
        
        return {"message": f"Habilidad '{habilidad}' eliminada correctamente"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")