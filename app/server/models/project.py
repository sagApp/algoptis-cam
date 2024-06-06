from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class ProjectStatus(str, Enum):
    TO_START = "To Start"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Project(BaseModel):
    id: str = Field(...)
    hash: str = Field(...)
    name: str = Field(...)
    hasAlerts: bool = Field(...)
    status: Optional[ProjectStatus]
    insertedAt: Optional[str]
    startedAt: Optional[str]
    camerasCount: Optional[int]
    cameras: Optional[list]
    sensors: Optional[list]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "hash": "abc123",
                "name": "Project Alpha",
                "hasAlerts": True,
                "status": "In Progress",
                "insertedAt": "2023-06-06T12:00:00Z",
                "startedAt": "2023-06-06T12:00:00Z",
                "camerasCount": 5,
                "cameras": [
                    # Exemples de caméras ici
                ],
                "sensors": [
                    # Exemples de capteurs ici
                ]
            }
        }

class UpdateProjectModel(BaseModel):
    id: Optional[str]
    hash: Optional[str]
    name: Optional[str]
    hasAlerts: Optional[bool]
    status: Optional[ProjectStatus]
    insertedAt: Optional[str]
    startedAt: Optional[str]
    camerasCount: Optional[int]
    cameras: Optional[list]
    sensors: Optional[list]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Project Alpha",
                "hasAlerts": True,
                "status": "In Progress",
                "insertedAt": "2023-06-06T12:00:00Z",
                "startedAt": "2023-06-06T12:00:00Z",
                "camerasCount": 5,
                "cameras": [
                    # Exemples de caméras ici
                ],
                "sensors": [
                    # Exemples de capteurs ici
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