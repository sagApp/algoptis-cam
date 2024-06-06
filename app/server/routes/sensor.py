# Importez les modules nécessaires
from fastapi import APIRouter, Body, Path
from fastapi.encoders import jsonable_encoder

# Importez les méthodes de la base de données pour les capteurs
from server.database import (
    add_sensor,
    delete_sensor,
    retrieve_sensor,
    retrieve_sensors,
    update_sensor,
)

# Importez les modèles de capteur
from server.models.sensor import (
    ErrorResponseModel,
    ResponseModel,
    Sensor,
    UpdateSensorModel,
)

# Créez un routeur FastAPI
router = APIRouter()

# Définissez les points de terminaison pour les opérations CRUD sur les capteurs
@router.post("/", response_description="Sensor data added into the database")
async def add_sensor_data(sensor: Sensor = Body(...)):
    sensor = jsonable_encoder(sensor)
    new_sensor = await add_sensor(sensor)
    return ResponseModel(new_sensor, "Sensor added successfully.")

@router.get("/", response_description="List all sensors")
async def get_sensors():
    sensors = await retrieve_sensors()
    return ResponseModel(sensors, "Sensors retrieved successfully.")

@router.get("/{sensor_id}", response_description="Get a single sensor by ID")
async def get_sensor(sensor_id: str = Path(..., title="The ID of the sensor to retrieve")):
    sensor = await retrieve_sensor(sensor_id)
    if sensor:
        return ResponseModel(sensor, "Sensor retrieved successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Sensor not found.")

@router.put("/{sensor_id}", response_description="Update a sensor by ID")
async def update_sensor_data(
    sensor_id: str = Path(..., title="The ID of the sensor to update"),
    request: UpdateSensorModel = Body(...),
):
    updated_sensor = await update_sensor(sensor_id, request.dict())
    if updated_sensor:
        return ResponseModel(
            f"Sensor with ID: {sensor_id} updated successfully",
            "Sensor updated successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Sensor with ID: {sensor_id}")

