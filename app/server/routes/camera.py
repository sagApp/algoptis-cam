# Importez les modules nécessaires
from fastapi import APIRouter, Body, Path
from fastapi.encoders import jsonable_encoder

# Importez les méthodes de la base de données pour les caméras
from server.database import (
    add_camera,
    delete_camera,
    retrieve_camera,
    retrieve_cameras,
    update_camera,
)

# Importez les modèles de caméra
from server.models.camera import (
    ErrorResponseModel,
    ResponseModel,
    Camera,
    UpdateCameraModel,
)

# Créez un routeur FastAPI
router = APIRouter()

# Définissez les points de terminaison pour les opérations CRUD sur les caméras
@router.post("/", response_description="Camera data added into the database")
async def add_camera_data(camera: Camera = Body(...)):
    camera = jsonable_encoder(camera)
    new_camera = await add_camera(camera)
    return ResponseModel(new_camera, "Camera added successfully.")

@router.get("/", response_description="List all cameras")
async def get_cameras():
    cameras = await retrieve_cameras()
    return ResponseModel(cameras, "Cameras retrieved successfully.")

@router.get("/{camera_id}", response_description="Get a single camera by ID")
async def get_camera(camera_id: str = Path(..., title="The ID of the camera to retrieve")):
    camera = await retrieve_camera(camera_id)
    if camera:
        return ResponseModel(camera, "Camera retrieved successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Camera not found.")

@router.put("/{camera_id}", response_description="Update a camera by ID")
async def update_camera_data(
    camera_id: str = Path(..., title="The ID of the camera to update"),
    request: UpdateCameraModel = Body(...),
):
    updated_camera = await update_camera(camera_id, request.dict())
    if updated_camera:
        return ResponseModel(
            f"Camera with ID: {camera_id} updated successfully",
            "Camera updated successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Camera with ID: {camera_id} not found")

@router.delete("/{camera_id}", response_description="Delete a camera by ID")
async def delete_camera_data(camera_id: str = Path(..., title="The ID of the camera to delete")):
    deleted_camera = await delete_camera(camera_id)
    if deleted_camera:
        return ResponseModel(
            f"Camera with ID: {camera_id} deleted successfully",
            "Camera deleted successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Camera with ID: {camera_id} not found")
