from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.path_utils import resource_path

app = FastAPI(title="POD5Plot")

app.mount(
    "/static",
    StaticFiles(
        directory=resource_path("app/static")
    ),
    name="static"
)

app.include_router(router)