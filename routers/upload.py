from fastapi import APIRouter, Request, File, UploadFile

from utils import files

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    dir_path = files.make_dir(".temp/missing_mods")
    contents = await file.read()
    with open(f"{dir_path}/{file.filename}", "wb") as f:
        f.write(contents)
    files.check_files(dir_path, "^.*.jar")
    return {
        "filename": file.filename
    }
