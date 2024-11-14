from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.db import logbooks_collection, geocaches_collection
from app.models.logbook import LogBook, LogBookInput

router = APIRouter()

@router.get("/getByEmail")
def get_logbook_by_email(email: str):
    logbooks = []
    
    query = {"email": email}

    logbooks_list = logbooks_collection.find(query).sort("stamp",-1)
    
    for logbook in logbooks_list:
        logbook["_id"] = str(logbook["_id"])
        logbooks.append(logbook)
        
    return JSONResponse(content=jsonable_encoder(logbooks), status_code=status.HTTP_200_OK)