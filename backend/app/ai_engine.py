"""
ai_engine.py - OpenRouter AI engine for NL → SQL
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

    prompt = f"""
You are an expert SQL query generator.

Convert the user's natural language request into a valid SQLite SQL query.

STRICT RULES:

1. Output ONLY raw SQL.
2. No markdown.
3. No explanations.
4. No backticks.
5. Never use DROP.
6. Never use ALTER.
7. Never use TRUNCATE.
8. Never use PRAGMA.
9. Never use ATTACH.
10. Never use DETACH.
11. UPDATE and DELETE must ALWAYS include a WHERE clause.
12. Use ONLY tables and columns from the provided schema.
13. If the request cannot be answered using the schema, output:
SELECT 'Not possible' AS message;

DATABASE SCHEMA:
{schema}

USER QUESTION:
{user_input}

SQL:
"""

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
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

        error_body = e.read().decode("utf-8", errors="replace")

        try:

            error_json = json.loads(error_body)

            error_info = error_json.get("error", {})

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

    cleaned = re.sub(
        r"```(?:sql)?",
        "",
        raw,
        flags=re.IGNORECASE
    )

    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.strip()

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
        "DELETE",
        "CREATE"
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

            if line.endswith(";"):
                break

    final_sql = " ".join(sql_lines).strip()

    return final_sql