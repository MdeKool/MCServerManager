from fastapi import APIRouter, Request, File, UploadFile, HTTPException

from utils import files

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    dir_path = files.make_dir(".temp/missing_mods")
    contents = await file.read()
    with open(f"{dir_path}/{file.filename}", "wb") as f:
        f.write(contents)
    if not files.check_zip_file(f"{dir_path}/{file.filename}", "^.*.jar"):
        return HTTPException(400, "All files in zip must be *.jar files")
    return {
        "filename": file.filename
    }
