from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db import logbooks_collection, geocaches_collection
from app.models.logbook import LogBook, LogBookInput


router = APIRouter()

@router.get("")
def get_logbooks():
    logbooks = []

    for logbook in logbooks_collection.find():
        logbook["_id"] = str(logbook["_id"])
        logbooks.append(logbook)
        
    return jsonable_encoder(logbooks)

@router.get("/getById")
def get_logbook(id: str):
    try:
        logbook = logbooks_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if logbook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logbook not found")
    
    logbook["_id"] = str(logbook["_id"])
    
    return JSONResponse(
        content=jsonable_encoder(logbook), 
        status_code=status.HTTP_200_OK
    )


@router.post("")
def create_logbook(logbook: LogBookInput):
    geocache = geocaches_collection.find_one({"_id": ObjectId(logbook.geocache_id)})

    if geocache is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logbook not found")

    logbook = LogBook(
        email=logbook.email,
        geocache_id=logbook.geocache_id,
        stamp=datetime.now()
    )
    
    logbook = jsonable_encoder(logbook)
    logbook_id = logbooks_collection.insert_one(logbook).inserted_id

    return JSONResponse(
        content={"message": "Logbook created", "_id": str(logbook_id)},
        status_code=status.HTTP_201_CREATED
    )


@router.delete("")
def delete_logbook(id: str):
    try:
        logbook = logbooks_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if logbook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Logbook not found")
    
    logbooks_collection.delete_one({"_id": ObjectId(id)})

    return JSONResponse(
        content={"message": "Logbook deleted"},
        status_code=status.HTTP_200_OK
    )


