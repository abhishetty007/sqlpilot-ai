from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

router = APIRouter()

UPLOAD_FOLDER = Path("uploaded_databases")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post("/upload-database")
async def upload_database(file: UploadFile = File(...)):
    destination = UPLOAD_FOLDER / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "filename": file.filename,
        "message": "Database uploaded successfully"
    }