from fastapi import APIRouter, Body, Path
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_project,
    delete_project,
    retrieve_project,
    retrieve_projects,
    update_project,
)
from server.models.project import (
    ErrorResponseModel,
    ResponseModel,
    Project,
    UpdateProjectModel,
)

router = APIRouter()

@router.post("/", response_description="Project data added into the database")
async def add_project_data(project: Project = Body(...)):
    project = jsonable_encoder(project)
    new_project = await add_project(project)
    return ResponseModel(new_project, "Project added successfully.")

@router.get("/", response_description="List all projects")
async def get_projects():
    projects = await retrieve_projects()
    return ResponseModel(projects, "Projects retrieved successfully.")

@router.get("/{project_id}", response_description="Get a single project by ID")
async def get_project(project_id: str = Path(..., title="The ID of the project to retrieve")):
    project = await retrieve_project(project_id)
    if project:
        return ResponseModel(project, "Project retrieved successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Project not found.")

@router.put("/{project_id}", response_description="Update a project by ID")
async def update_project_data(
    project_id: str = Path(..., title="The ID of the project to update"),
    request: UpdateProjectModel = Body(...),
):
    updated_project = await update_project(project_id, request.dict())
    if updated_project:
        return ResponseModel(
            f"Project with ID: {project_id} updated successfully",
            "Project updated successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Project with ID: {project_id} not found")

@router.delete("/{project_id}", response_description="Delete a project by ID")
async def delete_project_data(project_id: str = Path(..., title="The ID of the project to delete")):
    deleted_project = await delete_project(project_id)
    if deleted_project:
        return ResponseModel(
            f"Project with ID: {project_id} deleted successfully",
            "Project deleted successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Project with ID: {project_id} not found")
