from fastapi import APIRouter, Request, File, UploadFile

import util

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    dir_path = util.make_dir(".temp/missing_mods")
    contents = await file.read()
    with open(f"{dir_path}/{file.filename}", "wb") as f:
        f.write(contents)
    return {
        "filename": file.filename
    }
