from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import HTTPException

import smtplib
import ssl
from email.message import EmailMessage

from server.routes.document import router as DocumentSchema
from server.routes.translation import router as TranslationSchema


app = FastAPI()

app.include_router(DocumentSchema, tags=["Document"], prefix="/document")
app.include_router(TranslationSchema, tags=["Translation"], prefix="/translation")



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Translation office app!"}
