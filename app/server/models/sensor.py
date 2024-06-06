from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class SensorType(str, Enum):
    HEAT = "heat"
    GAS = "gas"
    HUMIDITY = "humidity"
    MOUVEMENT = "mouvement"

class SensorStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNDER_MAINTENANCE = "under_maintenance"

class Sensor(BaseModel):
    id: Optional[str]
    model: Optional[str]
    name: Optional[str]
    type: Optional[SensorType]
    status: Optional[SensorStatus]
    project: Optional[dict]
    location: Optional[dict]
    description: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "model": "Model XYZ",
                "name": "Sensor 1",
                "type": "heat",
                "status": "online",
                "project": {"id": 1, "name": "Project Alpha"},
                "location": {"lat": 40.7128, "lng": -74.0060},
                "description": "Description of the sensor"
            }
        }

class UpdateSensorModel(BaseModel):
    model: Optional[str]
    name: Optional[str]
    type: Optional[SensorType]
    status: Optional[SensorStatus]
    project: Optional[dict]
    location: Optional[dict]
    description: Optional[str]

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
