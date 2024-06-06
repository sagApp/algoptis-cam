from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId

class TranslationSchema(BaseModel):
    client_id: str = Field(...)
    work_status: str = Field(...)
    payment_status: str = Field(...)
    discount: float = Field(...)
    total_without_discount: float = Field(...)
    total: float = Field(...)
    rest: float = Field(...)
    payment: float = Field(...)
    documents: List[dict] = Field(...)
    payments: List[dict] = Field(...)
    
    
    class Config:
        #arbitrary_types_allowed=True
        json_schema_extra = {
            "example": {
                "client_id": "6574994048688dab9ff817ec",
                "work_status": "not_yet",
                "payment_status": "not_yet",
                "discount": 10.0,
                "total_without_discount": 8000.0,
                "total": 7200.0,
                "rest": 7200.0,
                "payment": 7200.0,
                "documents": [
                    {
                        "document_id": "5f4d5b7780bdfdf3bf47b890",
                        "language": "FR->ANG",
                        "price": 1000,
                        "nb_copies": 2
                    },
                    # Additional documents can be added here as dictionaries
                ],
               
                "payments": [
                    {
                        "price": 1000,
                        "created_at": "2024-01-27T09:07:43.106+00:00"
                    },
                    #Additional payments can be added here as dictionaries
                ]
                }
        }

class UpdateTranslationModel(BaseModel):
    work_status: Optional[str]
    payment_status: Optional[str]
    rest: Optional[float]
    payment: Optional[float]
    payments: Optional[List[dict]] = Field([])  # Define it as a list of dictionaries

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "5f4d5b7780bdfdf3bf47b890",
                "work_status": "in_progress",
                "payment_status": "pending",
                "discount": 15.0,
                "total_without_discount": 7500.0,
                "total": 6750.0,
                "rest": 6750.0,
                "payment": 500.0,
                "payments": [
                    {
                        "price": 1000,
                        "created_at": "2024-01-27T09:07:43.106+00:00"
                    }
                ]
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
