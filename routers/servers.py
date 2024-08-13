from fastapi import APIRouter, Request

from utils import instances

router = APIRouter(prefix="/servers")


@router.post("/on")
async def server_on(request: Request):
    data = await request.json()
    instance = data.get("instance")
    return instances.start_instance(instance)


@router.post("/off")
async def server_off(request: Request):
    data = await request.json()
    instance = data.get("instance")
    return instances.stop_instance(instance)


@router.post("/new")
async def server_new(request: Request):
    data = await request.json()
    return {
        "remaining_mods": instances.create_instance(**data)
    }
