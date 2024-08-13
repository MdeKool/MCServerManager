from fastapi import APIRouter, Request, File, UploadFile

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    contents = await file.read()
    print("Got a new file:", contents)
