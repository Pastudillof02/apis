from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db import tareas, colaboradores
from app.models.tarea import Tarea

router = APIRouter()

@router.get("")
def get_tareas():
    tareas_list = []
    for tarea in tareas.find():
        tarea["_id"] = str(tarea["_id"])
        tareas_list.append(tarea)

    return jsonable_encoder(tareas_list)


@router.get("/id/{id}")
def get_tarea(id: str):
    try:
        tarea = tareas.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    tarea["_id"] = str(tarea["_id"])

    return jsonable_encoder(tarea)

@router.post("")
def create_tarea(tarea: Tarea):
    tarea = jsonable_encoder(tarea)

    if colaboradores.find_one({"email": tarea["responsable"]}) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Responsable no encontrado")

    for c in tarea["colaboradores"]:
        if colaboradores.find_one({"email": c}) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Colaborador no encontrado")

    if len(tarea["colaboradores"]) > tarea["segmentos"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puede haber más colaboradores que segmentos")
    
    new_tarea = tareas.insert_one(tarea)
    created_tarea = tareas.find_one({"_id": new_tarea.inserted_id})

    if created_tarea is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al crear la tarea")
    
    created_tarea["_id"] = str(created_tarea["_id"])

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_tarea)


@router.put("/{id}")
def update_tarea(id: str, tarea: Tarea):
    try:
        existing_tarea = tareas.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if existing_tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    tarea = jsonable_encoder(tarea)

    if colaboradores.find_one({"email": tarea["responsable"]}) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Responsable no encontrado")

    for c in tarea["colaboradores"]:
        if colaboradores.find_one({"email": c}) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Colaborador no encontrado")

    tareas.update_one({"_id": ObjectId(id)}, {"$set": tarea})

    updated_tarea = tareas.find_one({"_id": ObjectId(id)})
    updated_tarea["_id"] = str(updated_tarea["_id"])

    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_tarea)


@router.delete("/{id}")
def delete_tarea(id: str):
    try:
        result = tareas.delete_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Tarea eliminada correctamente"})