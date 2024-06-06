from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import HTTPException

import smtplib
import ssl
from email.message import EmailMessage

from server.routes.project import router as ProjectSchema
from server.routes.camera import router as CameraSchema
from server.routes.sensor import router as SensorSchema


app = FastAPI()

app.include_router(ProjectSchema, tags=["Project"], prefix="/project")
app.include_router(CameraSchema, tags=["Camera"], prefix="/camera")
app.include_router(SensorSchema, tags=["Sensor"], prefix="/sensor")




@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Translation office app!"}
