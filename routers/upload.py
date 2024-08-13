from fastapi import APIRouter, Request, File, UploadFile

import util

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    dir_name = "~/.temp/missing_mods"
    util.make_dir(dir_name)
    contents = await file.read()
    with open(f"{dir_name}/{file.filename}", "wb+") as f:
        f.write(contents)
    return {
        "filename": file.filename
    }
