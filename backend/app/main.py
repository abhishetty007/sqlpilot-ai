from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.auth import login, signup, init_users_table
from app.upload import router as upload_router
from app.ai_engine import nl_to_sql_ai
from app.schema_reader import get_schema
from app.validator import validate_sql
from app.query_executor import execute_query


app = FastAPI(
    title="SQLPilot AI API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

init_users_table()


# =========================================================
# UPLOAD ROUTES
# =========================================================

app.include_router(upload_router)


# =========================================================
# REQUEST MODELS
# =========================================================

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class SQLRequest(BaseModel):
    prompt: str
    database: str


class ExecuteRequest(BaseModel):
    database: str
    sql: str


# =========================================================
# DATABASE NAME HELPER
# =========================================================

def normalize_database_name(database: str) -> str:

    database = database.strip()

    if not database:
        raise ValueError("Database name cannot be empty.")

    if not database.lower().endswith(".db"):
        database += ".db"

    return database


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to SQLPilot AI Backend 🚀"
    }


# =========================================================
# CREATE ACCOUNT
# =========================================================

@app.post("/register")
def register_user(data: RegisterRequest):

    success, message = signup(
        data.username,
        data.password
    )

    if not success:

        raise HTTPException(
            status_code=400,
            detail=message
        )

    return {
        "success": True,
        "message": message
    }


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login_user(data: LoginRequest):

    ok, user_id = login(
        data.username,
        data.password
    )

    if not ok:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "success": True,
        "user_id": user_id,
        "username": data.username
    }


# =========================================================
# GENERATE SQL
# =========================================================

@app.post("/generate-sql")
def generate_sql(data: SQLRequest):

    try:

        print("\n==============================")
        print("GENERATE SQL")
        print("==============================")

        database_name = normalize_database_name(
            data.database
        )

        print(
            "DATABASE FROM FRONTEND:",
            data.database
        )

        print(
            "NORMALIZED DATABASE:",
            database_name
        )

        print(
            "PROMPT:",
            data.prompt
        )

        schema = get_schema(
            database_name
        )

        print("SCHEMA:")
        print(schema)

        if not schema.strip():

            raise ValueError(
                f"No tables found in database '{database_name}'."
            )

        sql = nl_to_sql_ai(
            data.prompt,
            schema
        )

        print(
            "AI SQL:",
            sql
        )

        sql = validate_sql(
            sql
        )

        print(
            "VALIDATED SQL:",
            sql
        )

        print("==============================\n")

        return {
            "success": True,
            "sql": sql
        }

    except ValueError as e:

        print(
            "VALIDATION ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        print(
            "GENERATE SQL ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# EXECUTE SQL
# =========================================================

@app.post("/execute-sql")
def execute_sql(data: ExecuteRequest):

    try:

        print("\n==============================")
        print("EXECUTE SQL")
        print("==============================")

        database_name = normalize_database_name(
            data.database
        )

        print(
            "DATABASE FROM FRONTEND:",
            data.database
        )

        print(
            "NORMALIZED DATABASE:",
            database_name
        )

        print(
            "SQL FROM FRONTEND:",
            data.sql
        )

        sql = validate_sql(
            data.sql
        )

        print(
            "VALIDATED SQL:",
            sql
        )

        rows = execute_query(
            database_name,
            sql
        )

        print(
            "ROWS RETURNED:",
            len(rows)
        )

        print("==============================\n")

        return {
            "success": True,
            "rows": rows
        }

    except ValueError as e:

        print(
            "VALIDATION ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        print(
            "EXECUTE SQL ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )