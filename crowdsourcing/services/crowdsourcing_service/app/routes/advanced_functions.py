from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from app.db import tareas, colaboradores
from app.models.tarea import Tarea

router = APIRouter()

@router.get("/tareas/habilidades/{habilidad}")
def get_tareas_por_habilidad(habilidad: str):
    tareas_list = []
    for tarea in tareas.find():
        if habilidad in tarea["habilidades"]:
            tarea["_id"] = str(tarea["_id"])
            tareas_list.append(tarea)
        
    return jsonable_encoder(tareas_list)


@router.get("/tareas/colaborador/{email}")
def get_tareas_por_colaborador(email: EmailStr):
    tareas_list = []

    colaborador = colaboradores.find_one({"email": email})
    if colaborador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    for tarea in tareas.find():
        if email in tarea["colaboradores"]:
            tarea["_id"] = str(tarea["_id"])
            tareas_list.append(tarea)
        
    return jsonable_encoder(tareas_list)


@router.post("/tareas/{id}/colaborador/{email}")
def asignar_responsable(id: str, email: EmailStr):
    try:
        tarea = tareas.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    colaborador = colaboradores.find_one({"email": email})
    if colaborador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    for h in tarea["habilidades"]:
        if h not in colaborador["habilidades"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El colaborador no tiene las habilidades necessarias")
        
    result = tareas.update_one(
            {"_id": ObjectId(id)},
            {"$addToSet": {"colaboradores": colaborador["email"]}}
        )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
        
    return {"message": f"Responsable '{colaborador["email"]}' añadido correctamente"}
    

@router.get("/tareas/{id}/colaboradores")
def get_colaboradores_tarea(id: str):
    try:
        tarea = tareas.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if tarea is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    
    colaboradores_list = []

    for h in tarea["habilidades"]:
        for c in colaboradores.find():
            if h in c["habilidades"]:
                c["_id"] = str(c["_id"])
                colaboradores_list.append(c)
    
    return jsonable_encoder(colaboradores_list)


@router.get("/tareas/completas")
def get_tareas_completas():
    tareas_list = []
    for t in tareas.find():
        if len(t["colaboradores"]) == t["segmentos"]:
            t["_id"] = str(t["_id"])
            tareas_list.append(t)
    
    return jsonable_encoder(tareas_list)


@router.get("/colaboradores/{id}/colaboradores")
def get_colaboradores_colaborador(id: str):
    try:
        colaborador = colaboradores.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido")
    if colaborador is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
    
    colaboradores_list = []

    for t in tareas.find({"responsable": colaborador["email"]}):
        for c in t["colaboradores"]:
            if c not in colaboradores_list:       
                colaboradores_list.append(c)
    
    return jsonable_encoder(colaboradores_list)