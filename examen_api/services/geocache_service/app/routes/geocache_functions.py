from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from app.db import geocaches_collection

router = APIRouter()

@router.get("/getByHint")
def get_geocache_by_hint(hint: str):
    geocaches = []
    
    regex_pattern = f".*{hint}.*"
    query = {"hint": {"$regex": regex_pattern, "$options": "i"}}

    for geocache in geocaches_collection.find(query):
        geocache["_id"] = str(geocache["_id"])
        geocaches.append(geocache)
        
    return JSONResponse(content=jsonable_encoder(geocaches), status_code=status.HTTP_200_OK)