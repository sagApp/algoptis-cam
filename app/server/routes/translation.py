from fastapi import APIRouter, Body, Path
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_translation,
    delete_translation,
    retrieve_translation,
    retrieve_translations,
    update_translation,
)
from server.models.translation import (
    ErrorResponseModel,
    ResponseModel,
    TranslationSchema,
    UpdateTranslationModel,
)

router = APIRouter()

@router.post("/", response_description="Translation data added into the database")
async def add_translation_data(translation: TranslationSchema = Body(...)):
    translation = jsonable_encoder(translation)
    print(translation)
    new_translation = await add_translation(translation)
    return ResponseModel(new_translation, "Translation added successfully.")

@router.get("/", response_description="List all translations")
async def get_translations():
    translations = await retrieve_translations()
    return ResponseModel(translations, "Translations retrieved successfully.")

@router.get("/{translation_id}", response_description="Get a single translation by ID")
async def get_translation(translation_id: str = Path(..., title="The ID of the translation to retrieve")):
    translation = await retrieve_translation(translation_id)
    if translation:
        return ResponseModel(translation, "Translation retrieved successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Translation not found.")

@router.put("/{translation_id}", response_description="Update a translation by ID")
async def update_translation_data(
    translation_id: str = Path(..., title="The ID of the translation to update"),
    request: UpdateTranslationModel = Body(...),
):
    updated_translation = await update_translation(translation_id, request.dict())
    if updated_translation:
        return ResponseModel(
            f"Translation with ID: {translation_id} updated successfully",
            "Translation updated successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Translation with ID: {translation_id} not found")

@router.delete("/{translation_id}", response_description="Delete a translation by ID")
async def delete_translation_data(translation_id: str = Path(..., title="The ID of the translation to delete")):
    deleted_translation = await delete_translation(translation_id)
    if deleted_translation:
        return ResponseModel(
            f"Translation with ID: {translation_id} deleted successfully",
            "Translation deleted successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"Translation with ID: {translation_id} not found")


