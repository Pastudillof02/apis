from pydantic import BaseModel, HttpUrl

class Geocache(BaseModel):
    lat: float 
    lon: float 
    image: HttpUrl
    hint: str