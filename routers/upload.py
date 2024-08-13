from fastapi import APIRouter, Request, File, UploadFile

import util

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    util.make_dir("~/.temp/missing_mods")
    contents = await file.read()
    print(contents)
    with open(file.filename, "wb+") as f:
        f.write(contents)
    print("Write success")
    return {
        "filename": file.filename
    }
