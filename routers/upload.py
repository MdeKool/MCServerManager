from fastapi import APIRouter, Request

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(request: Request):
    print("Got a new file:", request.body())
