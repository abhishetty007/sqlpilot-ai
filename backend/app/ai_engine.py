"""
ai_engine.py - OpenRouter AI engine for NL → SQL
Improved schema-aware SQL generation
"""

import re
import urllib.request
import urllib.error
import json
import os

from dotenv import load_dotenv


# ============================================================
# LOAD .ENV RELIABLY
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# ============================================================
# OPENROUTER CONFIG
# ============================================================

MODEL = "openai/gpt-3.5-turbo"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ============================================================
# CHECK API KEY
# ============================================================

if not OPENROUTER_API_KEY:
    print("WARNING: OPENROUTER_API_KEY was not loaded.")
else:
    print("OpenRouter API key loaded successfully.")


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def nl_to_sql_ai(user_input: str, schema: str) -> str:

    if not OPENROUTER_API_KEY:
        raise Exception(
            "OpenRouter API key is missing. "
            "Make sure OPENROUTER_API_KEY is present in backend/.env"
        )

    if not schema or not schema.strip():
        raise Exception(
            "Database schema is empty. No tables are available."
        )

    # --------------------------------------------------------
    # Extract actual table names from schema
    # --------------------------------------------------------

    table_names = []

    for line in schema.splitlines():

        line = line.strip()

        if not line:
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)

        if match:
            table_names.append(match.group(1))

    available_tables = ", ".join(table_names)

    # --------------------------------------------------------
    # AI PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are SQLPilot, an expert SQLite SQL generator.

Your job is to convert the user's natural-language request into
ONE valid SQLite SQL query using ONLY the database schema provided below.

============================================================
CRITICAL DATABASE RULES
============================================================

1. You MUST use only tables that actually exist in the schema.

2. You MUST use only columns that actually exist in the schema.

3. NEVER invent a table name.

4. NEVER invent a column name.

5. NEVER assume that a natural-language word is a table name.

6. If the user says a common synonym, map it to the closest
   ACTUAL table in the schema.

Examples:

   "movies" / "films" / "film" -> film
   "customers" / "customer" -> customer
   "actors" / "actor" -> actor
   "payments" / "payment" -> payment
   "rentals" / "rental" -> rental
   "staff" / "employees" -> staff
   "stores" / "store" -> store
   "cities" / "city" -> city
   "countries" / "country" -> country
   "addresses" / "address" -> address
   "languages" / "language" -> language
   "categories" / "category" -> category
   "inventory" / "items" -> inventory ONLY when the
   user's request clearly refers to inventory items.

IMPORTANT:
Do NOT blindly create a table from the user's wording.

For example, if the schema contains:

film(film_id, title, ...)

and the user asks:

"show all movies"

the correct query is:

SELECT * FROM film;

NOT:

SELECT * FROM movie;

Similarly, if the user asks:

"show all items"

and the schema contains inventory but does NOT contain item,
use the closest appropriate existing table only if the meaning
clearly refers to inventory. Otherwise return:

SELECT 'Not possible' AS message;

============================================================
SCHEMA
============================================================

{schema}

============================================================
ACTUAL TABLES AVAILABLE
============================================================

{available_tables}

============================================================
QUERY SAFETY RULES
============================================================

1. Output ONLY raw SQL.
2. Do NOT output markdown.
3. Do NOT output explanations.
4. Do NOT use backticks.
5. Generate exactly ONE SQL statement.
6. Never use DROP.
7. Never use ALTER.
8. Never use TRUNCATE.
9. Never use PRAGMA.
10. Never use ATTACH.
11. Never use DETACH.
12. Never use VACUUM.
13. Never use REINDEX.
14. Never use CREATE.
15. UPDATE queries MUST contain WHERE.
16. DELETE queries MUST contain WHERE.
17. INSERT is allowed only when the required table and columns
    actually exist in the schema.
18. SELECT queries may use JOINs only when the required
    tables and columns actually exist.
19. Never reference a table or column that is not present
    in the schema.

============================================================
HANDLING IMPOSSIBLE REQUESTS
============================================================

If the user's request cannot be answered using the available
tables and columns, output exactly:

SELECT 'Not possible' AS message;

Do NOT invent a table or column to satisfy the request.

============================================================
USER QUESTION
============================================================

{user_input}

============================================================
RETURN SQL ONLY
============================================================
"""

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You generate safe SQLite SQL. "
                    "You must strictly follow the supplied database schema."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.0,
        "max_tokens": 300
    }).encode("utf-8")

    request = urllib.request.Request(
        OPENROUTER_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "SQLPilot AI"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            response_data = json.loads(
                response.read().decode("utf-8")
            )

        # ====================================================
        # RESPONSE VALIDATION
        # ====================================================

        choices = response_data.get("choices")

        if not choices:
            raise Exception(
                f"OpenRouter returned no choices: {response_data}"
            )

        message = choices[0].get("message", {})

        raw_sql = message.get("content")

        if not raw_sql:
            raise Exception(
                "OpenRouter returned empty content."
            )

        if not isinstance(raw_sql, str):
            raise Exception(
                "OpenRouter response was not text."
            )

        cleaned_sql = _clean(raw_sql)

        if not cleaned_sql:
            raise Exception(
                "Could not extract SQL from AI response."
            )

        return cleaned_sql

    except urllib.error.HTTPError as e:

        error_body = e.read().decode(
            "utf-8",
            errors="replace"
        )

        try:

            error_json = json.loads(error_body)

            error_info = error_json.get(
                "error",
                {}
            )

            message = error_info.get(
                "message",
                error_body
            )

        except Exception:

            message = error_body

        raise Exception(
            f"OpenRouter HTTP {e.code}: {message}"
        )

    except urllib.error.URLError as e:

        raise Exception(
            f"Network error connecting to OpenRouter: {e.reason}"
        )

    except Exception as e:

        raise Exception(
            f"AI Engine Error: {str(e)}"
        )


# ============================================================
# SQL CLEANER
# ============================================================

def _clean(raw: str) -> str:

    if not raw:
        return ""

    # Remove markdown code fences
    cleaned = re.sub(
        r"```(?:sql)?",
        "",
        raw,
        flags=re.IGNORECASE
    )

    cleaned = cleaned.replace(
        "```",
        ""
    )

    cleaned = cleaned.replace(
        "`",
        ""
    )

    cleaned = cleaned.strip()

    # --------------------------------------------------------
    # Split lines
    # --------------------------------------------------------

    lines = [
        line.strip()
        for line in cleaned.splitlines()
        if line.strip()
    ]

    sql_lines = []

    capture = False

    VALID_STARTS = (
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE"
    )

    for line in lines:

        upper = line.upper()

        words = upper.split()

        if not words:
            continue

        first_word = words[0]

        if first_word in VALID_STARTS:
            capture = True

        if capture:

            sql_lines.append(line)

            if ";" in line:
                break

    final_sql = " ".join(
        sql_lines
    ).strip()

    # --------------------------------------------------------
    # Remove accidental trailing explanation
    # --------------------------------------------------------

    if ";" in final_sql:

        final_sql = final_sql.split(
            ";",
            1
        )[0].strip() + ";"

    return final_sql