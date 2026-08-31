from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import sqlite3

router = APIRouter()

UPLOAD_FOLDER = Path("uploaded_databases")
UPLOAD_FOLDER.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════
# UPLOAD DATABASE
# ═══════════════════════════════════════════════

@router.post("/upload-database")
async def upload_database(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    allowed_extensions = (
        ".db",
        ".sqlite",
        ".sqlite3"
    )

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only SQLite database files are allowed."
        )

    destination = UPLOAD_FOLDER / file.filename

    try:

        with open(destination, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return {
            "success": True,
            "filename": file.filename,
            "message": "Database uploaded successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


# ═══════════════════════════════════════════════
# GET DATABASES
# ═══════════════════════════════════════════════

@router.get("/databases")
async def get_databases():

    databases = []

    for file in UPLOAD_FOLDER.glob("*.db"):

        databases.append({
            "name": file.stem,
            "filename": file.name
        })

    return databases


# ═══════════════════════════════════════════════
# GET TABLES
# ═══════════════════════════════════════════════

@router.get("/tables/{database_name}")
async def get_tables(database_name: str):

    db_path = UPLOAD_FOLDER / database_name

    print("TABLE REQUEST:", database_name)
    print("DATABASE PATH:", db_path)
    print("EXISTS:", db_path.exists())

    if not db_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Database not found."
        )

    try:

        conn = sqlite3.connect(db_path)

        cur = conn.cursor()

        cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        tables = [
            row[0]
            for row in cur.fetchall()
        ]

        conn.close()

        print("TABLES FOUND:", tables)

        return {
            "database": database_name,
            "tables": tables
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not read database: {str(e)}"
        )


# ═══════════════════════════════════════════════
# DELETE DATABASE
# ═══════════════════════════════════════════════

@router.delete("/databases/{database_name}")
async def delete_database(database_name: str):

    # Security: only allow the filename, not paths
    database_name = Path(database_name).name

    db_path = UPLOAD_FOLDER / database_name

    print("DELETE DATABASE:", database_name)
    print("DATABASE PATH:", db_path)

    if not db_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Database not found."
        )

    if not db_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="Invalid database."
        )

    try:

        db_path.unlink()

        print("DATABASE DELETED:", database_name)

        return {
            "success": True,
            "message": f"{database_name} removed successfully."
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not remove database: {str(e)}"
        )