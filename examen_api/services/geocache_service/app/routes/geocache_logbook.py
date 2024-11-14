from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status
from app.db import geocaches_collection, logbooks_collection

router = APIRouter()

@router.get("/notFounds")
def get_not_found_geocaches():
    geocaches = []

    for geocache in geocaches_collection.find():
        if logbooks_collection.find_one({"geocache_id": str(geocache["_id"])}) is None:
            geocache["_id"] = str(geocache["_id"])
            geocaches.append(geocache)
        
    return JSONResponse(content=jsonable_encoder(geocaches), status_code=status.HTTP_200_OK)
