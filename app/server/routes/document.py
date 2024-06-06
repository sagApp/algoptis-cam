from fastapi import APIRouter, Body, Path
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_document,
    delete_document,
    retrieve_document,
    retrieve_documents,
    update_document,
)
from server.models.document import ( # type: ignore
    ErrorResponseModel,
    ResponseModel,
    DocumentSchema,
    UpdateDocumentModel,
)

router = APIRouter()

@router.post("/", response_description="Document data added into the database")
async def add_document_data(document: DocumentSchema = Body(...)):
    document = jsonable_encoder(document)
    new_document = await add_document(document)
    return ResponseModel(new_document, "document added successfully.")


@router.get("/", response_description="List all documents")
async def get_documents():
    documents = await retrieve_documents()
    return ResponseModel(documents, "documents retrieved successfully.")

@router.get("/{document_id}", response_description="Get a single document by ID")
async def get_document(document_id: str = Path(..., title="The ID of the document to retrieve")):
    document = await retrieve_document(document_id)
    if document:
        return ResponseModel(document, "document retrieved successfully.")
    return ErrorResponseModel("An error occurred.", 404, "document not found.")

@router.put("/{document_id}", response_description="Update a document by ID")
async def update_document_data(
    document_id: str = Path(..., title="The ID of the document to update"),
    request: UpdateDocumentModel = Body(...),
):
    updated_document = await update_document(document_id, request.dict())
    if updated_document:
        return ResponseModel(
            f"document with ID: {document_id} updated successfully",
            "document updated successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"document with ID: {document_id} not found")

@router.delete("/{document_id}", response_description="Delete a document by ID")
async def delete_document_data(document_id: str = Path(..., title="The ID of the document to delete")):
    deleted_document = await delete_document(document_id)
    if deleted_document:
        return ResponseModel(
            f"document with ID: {document_id} deleted successfully",
            "document deleted successfully",
        )
    return ErrorResponseModel("An error occurred", 404, f"document with ID: {document_id} not found")