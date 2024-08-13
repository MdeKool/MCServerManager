from fastapi import APIRouter, Request, File, UploadFile

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(request: Request, file: UploadFile = File(...)):
    print(request.form())
    contents = await file.read()
    print("Got a new file:", contents)
