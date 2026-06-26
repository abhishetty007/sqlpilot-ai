"""
validator.py - SQL Query Validator
Allowed:  SELECT, INSERT, UPDATE (with WHERE), DELETE (with WHERE), CREATE TABLE
Blocked:  DROP, TRUNCATE, ALTER, PRAGMA, UPDATE/DELETE without WHERE
"""

import re

DANGEROUS = ["DROP", "TRUNCATE", "ALTER", "ATTACH", "DETACH", "PRAGMA", "EXEC","VACCUM","REINDEX","ANALYZE"]


def classify_query(sql: str) -> dict:
    if not sql or not sql.strip():
        return {"type": "UNKNOWN", "allowed": False, "reason": "Query is empty."}

    clean = sql.strip()
    upper = clean.upper()
    if clean.count(";") > 1:

     return {
        "type": "DANGEROUS",
        "allowed": False,
        "reason": "🚫 Multiple SQL statements are not allowed."
    }    
    words = upper.split()
    first = words[0] if words else ""
    second = words[1] if len(words) > 1 else ""

    # Hard block dangerous keywords
    for kw in DANGEROUS:
        if re.search(rf"\b{kw}\b", upper):
            return {"type": "DANGEROUS", "allowed": False,
                    "reason": f"🚫 '{kw}' is permanently blocked — it can cause irreversible damage."}

    if first == "SELECT":
        return {"type": "SELECT", "allowed": True, "reason": "✅ Safe read query."}

    if first == "INSERT":
        return {"type": "INSERT", "allowed": True, "reason": "✅ Insert operation allowed."}

    if first == "UPDATE":

        if not re.search(r"\bWHERE\b", upper):

            return {
                "type": "UPDATE",
                "allowed": False,
                "reason": "⚠️ UPDATE without WHERE is blocked — it would modify ALL rows."
            }

        dangerous_patterns = [
            r"WHERE\s+1\s*=\s*1",
            r"WHERE\s+ID\s+IS\s+NOT\s+NULL",
            r"WHERE\s+TRUE"
        ]

        for pattern in dangerous_patterns:

            if re.search(pattern, upper):

                return {
                    "type": "UPDATE",
                    "allowed": False,
                    "reason": "🚫 Dangerous mass UPDATE detected and blocked."
                }

        return {
            "type": "UPDATE",
            "allowed": True,
            "reason": "✅ Update operation allowed."
        }


    if first == "DELETE":

        if not re.search(r"\bWHERE\b", upper):

            return {
                "type": "DELETE",
                "allowed": False,
                "reason": "⚠️ DELETE without WHERE is blocked — it would delete ALL rows."
            }

        dangerous_patterns = [
            r"WHERE\s+1\s*=\s*1",
            r"WHERE\s+ID\s+IS\s+NOT\s+NULL",
            r"WHERE\s+TRUE"
        ]

        for pattern in dangerous_patterns:

            if re.search(pattern, upper):

                return {
                    "type": "DELETE",
                    "allowed": False,
                    "reason": "🚫 Dangerous mass DELETE detected and blocked."
                }

        return {
            "type": "DELETE",
            "allowed": True,
            "reason": "✅ Delete operation allowed."
        }
    if first == "CREATE" and second == "TABLE":
        return {"type": "CREATE", "allowed": True, "reason": "✅ Create table operation allowed."}

    return {"type": "UNKNOWN", "allowed": False,
            "reason": f"❌ Unrecognized query type '{first}'. Allowed: SELECT, INSERT, UPDATE, DELETE, CREATE TABLE."}


def validate_and_report(sql: str) -> dict:
    result = classify_query(sql)
    result["is_valid"] = result["allowed"]
    result["message"] = result["reason"]
    result["sql"] = sql.strip()
    return result