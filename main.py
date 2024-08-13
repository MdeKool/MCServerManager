from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from routers import servers, modals, upload
from utils import instances

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.include_router(servers.router)
app.include_router(modals.router)
app.include_router(upload.router)

app.mount("/js", StaticFiles(directory="js"), name="scripts")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/styling", StaticFiles(directory="static/styling"), name="styling")


@app.get("/")
async def root(request: Request):
    live_list = list_servers()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "instances": live_list,
        }
    )


def list_servers():
    all_instances = instances.get_instances()
    live_instances = instances.get_live_instances()
    port_dict = {i[0]: i[1] for i in live_instances}
    live_list = [(name, True, port_dict[name]) if name in port_dict else (name, False) for name in all_instances]
    return live_list
