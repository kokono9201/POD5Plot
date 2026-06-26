from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.path_utils import resource_path

router = APIRouter()

templates = Jinja2Templates(
    directory=resource_path("app/templates")
)


@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )