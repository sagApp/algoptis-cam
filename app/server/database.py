import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime
from typing import List
#from server.external.email import send_email

from os import environ as env

MONGO_DETAILS = env.get('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cam

################################################# Project ########################################

project_collection = database.get_collection("projects")


def project_helper(project) -> dict:
    return {
        "id": str(project["_id"]),
        "hash": project["hash"],
        "name": project["name"],
        "hasAlerts": project["hasAlerts"],
        "status": project.get("status"),
        "insertedAt": project.get("insertedAt"),
        "startedAt": project.get("startedAt"),
        "camerasCount": project.get("camerasCount"),
        "cameras": project.get("cameras"),
        "sensors": project.get("sensors")
    }


async def retrieve_projects():
    projects = []
    async for project in project_collection.find():
        projects.append(project_helper(project))
    return projects


async def add_project(project_data: dict) -> dict:
    project_data["insertedAt"] = datetime.utcnow()
    project_data["startedAt"] = datetime.utcnow()

    project = await project_collection.insert_one(project_data)
    new_project = await project_collection.find_one({"_id": project.inserted_id})
    return project_helper(new_project)


async def retrieve_project(id: str) -> dict:
    project = await project_collection.find_one({"_id": ObjectId(id)})
    if project:
        return project_helper(project)


async def update_project(id: str, data: dict):
    if len(data) < 1:
        return False

    data["updatedAt"] = datetime.utcnow()

    project = await project_collection.find_one({"_id": ObjectId(id)})
    if project:
        updated_project = await project_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_project:
            return True
        return False


async def delete_project(id: str):
    project = await project_collection.find_one({"_id": ObjectId(id)})
    if project:
        await project_collection.delete_one({"_id": ObjectId(id)})
        return True


################################################# Camera ########################################

camera_collection = database.get_collection("cameras")


def camera_helper(camera) -> dict:
    return {
        "id": str(camera["_id"]),
        "thumbnailUrl": camera["thumbnailUrl"],
        "modelName": camera["modelName"],
        "project": camera.get("project"),
        "location": camera.get("location"),
        "model": camera.get("model"),
        "description": camera.get("description"),
        "adjustableCoverage": camera.get("adjustableCoverage"),
        "status": camera["status"],
        "isOnline": camera.get("isOnline"),
        "offlineReason": camera.get("offlineReason"),
        "lastOnlineAt": camera.get("lastOnlineAt"),
        "name": camera.get("name"),
        "createdAt": camera.get("createdAt")
    }


async def retrieve_cameras():
    cameras = []
    async for camera in camera_collection.find():
        cameras.append(camera_helper(camera))
    return cameras


async def add_camera(camera_data: dict) -> dict:
    camera_data["createdAt"] = datetime.utcnow()

    camera = await camera_collection.insert_one(camera_data)
    new_camera = await camera_collection.find_one({"_id": camera.inserted_id})
    return camera_helper(new_camera)


async def retrieve_camera(id: str) -> dict:
    camera = await camera_collection.find_one({"_id": ObjectId(id)})
    if camera:
        return camera_helper(camera)


async def update_camera(id: str, data: dict):
    if len(data) < 1:
        return False

    data["updatedAt"] = datetime.utcnow()

    camera = await camera_collection.find_one({"_id": ObjectId(id)})
    if camera:
        updated_camera = await camera_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_camera:
            return True
        return False


async def delete_camera(id: str):
    camera = await camera_collection.find_one({"_id": ObjectId(id)})
    if camera:
        await camera_collection.delete_one({"_id": ObjectId(id)})
        return True


################################################# Sensor ########################################

sensor_collection = database.get_collection("sensors")


def sensor_helper(sensor) -> dict:
    return {
        "id": str(sensor["_id"]),
        "model": sensor["model"],
        "name": sensor["name"],
        "type": sensor["type"],
        "status": sensor["status"],
        "project": sensor.get("project"),
        "location": sensor.get("location"),
        "description": sensor.get("description"),
    }


async def retrieve_sensors():
    sensors = []
    async for sensor in sensor_collection.find():
        sensors.append(sensor_helper(sensor))
    return sensors


async def add_sensor(sensor_data: dict) -> dict:
    sensor = await sensor_collection.insert_one(sensor_data)
    new_sensor = await sensor_collection.find_one({"_id": sensor.inserted_id})
    return sensor_helper(new_sensor)


async def retrieve_sensor(id: str) -> dict:
    sensor = await sensor_collection.find_one({"_id": ObjectId(id)})
    if sensor:
        return sensor_helper(sensor)


async def update_sensor(id: str, data: dict):
    if len(data) < 1:
        return False

    sensor = await sensor_collection.find_one({"_id": ObjectId(id)})
    if sensor:
        updated_sensor = await sensor_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_sensor:
            return True
        return False


async def delete_sensor(id: str):
    sensor = await sensor_collection.find_one({"_id": ObjectId(id)})
    if sensor:
        await sensor_collection.delete_one({"_id": ObjectId(id)})
        return True
