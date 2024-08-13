from fastapi import APIRouter, Request, File

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(request: Request):
    print("Got a new file:", File(await request.body()))
