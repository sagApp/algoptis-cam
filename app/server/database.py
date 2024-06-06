import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime
import pandas as pd
from typing import List
from server.externel.email import send_email 
 
from os import environ as env


MONGO_DETAILS = env.get('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.translation


#################################################   Document ########################################
document_collection = database.get_collection("documents")

# helpers

def document_helper(document) -> dict:
    return {
        "id": str(document["_id"]),
        "name": document["name"],
        "description": document["description"],
        "createdAt": document.get("createdAt", None),
        "updatedAt": document.get("updatedAt", None), 

    }
    

# Retrieve all documents present in the database
async def retrieve_documents():
    documents = []
    async for document in document_collection.find():
        documents.append(document_helper(document))
    return documents


# Add a new document into the database
async def add_document(document_data: dict) -> dict:
    document_data["created_at"] = datetime.utcnow()
    document_data["updated_at"] = datetime.utcnow()
    
    document = await document_collection.insert_one(document_data)
    new_document = await document_collection.find_one({"_id": document.inserted_id})
    return document_helper(new_document)

# Retrieve a document with a matching ID
async def retrieve_document(id: str) -> dict:
    document = await document_collection.find_one({"_id": ObjectId(id)})
    if document:
        return document_helper(document)


# Update a document with a matching ID
async def update_document(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    
    data["updated_at"] = datetime.utcnow()
    
    document = await document_collection.find_one({"_id": ObjectId(id)})
    if document:
        updated_document = await document_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_document:
            return True
        return False


# Delete a document from the database
async def delete_document(id: str):
    document = await document_collection.find_one({"_id": ObjectId(id)})
    if document:
        await document_collection.delete_one({"_id": ObjectId(id)})
        return True
    
    

######################################  translation ############################

translation_collection = database.get_collection("translations")


def translation_helper(translation) -> dict:
    return {
        "id": str(translation["_id"]),
        "client_id": str(translation["client_id"]),
        "work_status": translation["work_status"],
        "payment_status": translation["payment_status"],
        "discount": translation["discount"],
        "total_without_discount": translation["total_without_discount"],
        "total": translation["total"],
        "rest": translation["rest"],
        "payment": translation["payment"],
        "created_at": translation.get("created_at", None),
        "updated_at": translation.get("updated_at", None),
        "documents": translation["documents"],
        "payments": translation["payments"]
    }


async def retrieve_translations() -> List[dict]:
    translations = []
    async for translation in translation_collection.find():
        translations.append(translation_helper(translation))
    return translations


async def add_translation(translation_data: dict) -> dict:
    translation_data["created_at"] = datetime.utcnow()
    translation_data["updated_at"] = datetime.utcnow()

    translation = await translation_collection.insert_one(translation_data)
    new_translation = await translation_collection.find_one({"_id": translation.inserted_id})
    return translation_helper(new_translation)


async def retrieve_translation(id: str) -> dict:
    translation = await translation_collection.find_one({"_id": ObjectId(id)})
    if translation:
        return translation_helper(translation)


async def update_translation(id: str, data: dict):
    if len(data) < 1:
        return False

    # Add current datetime
    current_datetime = datetime.utcnow()
    data["updated_at"] = current_datetime

    #Prepare payment data to be appended to payments array
    payment_data = {
        "price":  data["payment"],
        "created_at": current_datetime
    }

    # Find the translation
    translation = await translation_collection.find_one({"_id": ObjectId(id)})
    if translation:
        # Merging existing payments with new payment
        payments = translation.get('payments', [])
        payments.append(payment_data)
        data["payments"] = payments
        old_payment = translation.get('payment')
        new_payment = old_payment + data["payment"]
        data["payment"] = new_payment
        # Update the translation
        updated_translation = await translation_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_translation:
            send_email(payment_data["price"])
            return True

    return False



async def delete_translation(id: str):
    translation = await translation_collection.find_one({"_id": ObjectId(id)})
    if translation:
        await translation_collection.delete_one({"_id": ObjectId(id)})
        return True
    
    

