from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="Compliance Checker API - Project 2")
app.include_router(router)
