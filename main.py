from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="POD5Plot")

app.include_router(router)