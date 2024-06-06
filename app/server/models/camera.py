from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class CameraStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    OFFLINE_SCHEDULED = "offline_scheduled"
    WAITING = "waiting"
    UNDER_MAINTENANCE = "under_maintenance"

class Camera(BaseModel):
    thumbnailUrl: Optional[str] = Field(...)
    modelName: Optional[str]
    project: Optional[dict]
    location: Optional[dict]
    model: Optional[str]
    description: Optional[str]
    adjustableCoverage: Optional[bool]  # TODO: Should add a positioning system 
    status: CameraStatus
    isOnline: Optional[bool]
    offlineReason: Optional[str]
    lastOnlineAt: Optional[str]
    name: Optional[str]
    createdAt: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "thumbnailUrl": "http://example.com/thumbnail.jpg",
                "modelName": "Model XYZ",
                "project": {"id": "6661ad4c839f321df5b839a8", "name": "Project Alpha"},
                "location": {"lat": 40.7128, "lng": -74.0060},
                "model": "Model ABC",
                "description": "Description of the camera",
                "adjustableCoverage": True,
                "status": "online",
                "isOnline": True,
                "offlineReason": None,
                "lastOnlineAt": "2024-06-07T12:00:00Z",
                "name": "Camera 1",
                "createdAt": "2024-06-01T12:00:00Z"
            }
        }
        
class UpdateCameraModel(BaseModel):
    thumbnailUrl: Optional[str]
    modelName: Optional[str]
    project: Optional[dict]
    location: Optional[dict]
    model: Optional[str]
    description: Optional[str]
    adjustableCoverage: Optional[bool]
    status: Optional[str]
    isOnline: Optional[bool]
    offlineReason: Optional[str]
    lastOnlineAt: Optional[str]
    name: Optional[str]
    createdAt: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "thumbnailUrl": "http://example.com/thumbnail.jpg",
                "modelName": "Model XYZ",
                "project": {"id": 1, "name": "Project Alpha"},
                "location": {"lat": 40.7128, "lng": -74.0060},
                "model": "Model ABC",
                "description": "Description of the camera",
                "adjustableCoverage": True,
                "status": "online",
                "isOnline": True,
                "offlineReason": None,
                "lastOnlineAt": "2024-06-07T12:00:00Z",
                "name": "Camera 1",
                "createdAt": "2024-06-01T12:00:00Z"
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