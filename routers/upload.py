from fastapi import APIRouter, Request, File, UploadFile

import util

router = APIRouter(prefix="/upload")


@router.post("/")
async def file_upload(file: UploadFile = File(...)):
    util.make_dir("~/.temp/missing_mods")
    await file.write()
    return {
        "filename": file.filename
    }
