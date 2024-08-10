from fastapi import APIRouter, Request

import util

router = APIRouter(prefix="/servers")


@router.post("/on")
async def server_on(request: Request):
    data = await request.json()
    instance = data.get("instance")
    return util.start_instance(instance)


@router.post("/off")
async def server_off(request: Request):
    data = await request.json()
    instance = data.get("instance")
    return util.stop_instance(instance)


@router.post("/new")
async def server_new(request: Request):
    data = await request.json()
    return util.create_instance(**data)
