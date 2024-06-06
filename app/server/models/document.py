from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class DocumentSchema(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


    class Config:
        json_schema_extra = {
            "example": {
                "name": "Attestation de Travail",
                "description": "traduction attestation de travail simple",
                # created_at and updated_at will be automatically set to the current UTC time
            }
        }
        
class UpdateDocumentModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Attestation de Travail",
                "description": "traduction attestation de travail simple",
                # updated_at will be automatically set to the current UTC time
            }
        }
        

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
