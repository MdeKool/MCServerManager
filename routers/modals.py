from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

import util

templates = Jinja2Templates(directory="templates/modals")
router = APIRouter(prefix="/modals")


@router.get("/new_instance")
async def new_instance(request: Request):
    return {
        "modal": templates.TemplateResponse("new_instance.html", {"request": request}).body.decode(),
        "loaders": util.get_loaders()
    }
