"""
ai_engine.py - AI Fallback using OpenRouter API
Stable version with better error handling and response safety.
"""

import re
import urllib.request
import urllib.error
import json

# ==============================
# OpenRouter Configuration
# ==============================

from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# More stable free model
MODEL = "openai/gpt-3.5-turbo"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ==============================
# Main AI Function
# ==============================

def nl_to_sql_ai(user_input: str, schema: str) -> str:

    prompt = f"""
You are an expert SQL query generator.

Convert the user's natural language request into a valid SQLite SQL query.

STRICT RULES:
1. Output ONLY raw SQL.
2. No markdown.
3. No explanations.
4. No backticks.
5. Never use DROP, ALTER, TRUNCATE, PRAGMA, ATTACH, DETACH.
6. UPDATE and DELETE must ALWAYS include WHERE clause.
7. Use ONLY tables and columns from schema.
8. If impossible, output:
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
        "max_tokens": 200
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "NL-to-SQL System"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(req, timeout=30) as response:

            response_data = json.loads(
                response.read().decode("utf-8")
            )

            # ==============================
            # SAFE RESPONSE HANDLING
            # ==============================

            choices = response_data.get("choices", [])

            if not choices:
                raise Exception("AI returned no choices.")

            message = choices[0].get("message", {})

            raw_sql = message.get("content")

            if not raw_sql:
                raise Exception("AI returned empty content.")

            if not isinstance(raw_sql, str):
                raise Exception("AI response is not valid text.")

            cleaned_sql = _clean(raw_sql)

            if not cleaned_sql:
                raise Exception("Could not extract valid SQL.")

            return cleaned_sql

    except urllib.error.HTTPError as e:

        err_body = e.read().decode("utf-8")

        try:
            err_json = json.loads(err_body)
            msg = err_json.get("error", {}).get("message", err_body)
        except Exception:
            msg = err_body

        raise Exception(f"OpenRouter HTTP {e.code}: {msg}")

    except urllib.error.URLError as e:

        raise Exception(f"Network Error: {e.reason}")

    except Exception as e:

        raise Exception(f"AI Engine Error: {str(e)}")


# ==============================
# SQL Cleaner
# ==============================

def _clean(raw: str) -> str:

    if not raw:
        return ""

    # Remove markdown blocks
    cleaned = re.sub(
        r"```(?:sql)?",
        "",
        raw,
        flags=re.IGNORECASE
    )

    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.strip()

    # Split lines
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

        first_word = upper.split()[0] if upper.split() else ""

        if first_word in VALID_STARTS:
            capture = True

        if capture:
            sql_lines.append(line)

            if line.endswith(";"):
                break

    final_sql = " ".join(sql_lines).strip()

    return final_sql

