from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from app.db import geocaches_collection
from app.models.geocache import Geocache

router = APIRouter()

@router.get("")
def get_geocaches():
    geocaches = []

    for geocache in geocaches_collection.find():
        geocache["_id"] = str(geocache["_id"])
        geocaches.append(geocache)
        
    return jsonable_encoder(geocaches)


@router.get("/getById")
def get_geocache(id: str):
    try:
        geocache = geocaches_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if geocache is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Geocache not found")
    
    geocache["_id"] = str(geocache["_id"])
    
    return JSONResponse(
        content=jsonable_encoder(geocache), 
        status_code=status.HTTP_200_OK
    )


@router.post("")
def create_geocache(geocache: Geocache):
    geocache = jsonable_encoder(geocache)
    geocache_id = geocaches_collection.insert_one(geocache).inserted_id

    return JSONResponse(
        content={"message": "Geocache created", "_id": str(geocache_id)},
        status_code=status.HTTP_201_CREATED
    )


@router.delete("")
def delete_geocache(id: str):
    try:
        geocache = geocaches_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    
    if geocache is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Geocache not found")
    
    geocaches_collection.delete_one({"_id": ObjectId(id)})

    return JSONResponse(
        content={"message": "Geocache deleted"},
        status_code=status.HTTP_200_OK
    )

