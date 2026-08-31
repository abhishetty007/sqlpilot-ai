import re


def validate_sql(sql: str) -> str:
    """
    Validate SQL before execution.

    Allowed:
    - SELECT
    - INSERT
    - UPDATE
    - DELETE

    Blocked:
    - DROP
    - ALTER
    - TRUNCATE
    - PRAGMA
    - ATTACH
    - DETACH
    - VACUUM
    - REINDEX
    - CREATE

    UPDATE and DELETE must contain WHERE.
    Multiple SQL statements are not allowed.
    """

    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not sql or not isinstance(sql, str):

        raise ValueError(
            "SQL is empty or invalid."
        )

    # =====================================================
    # CLEAN AI RESPONSE
    # =====================================================

    sql = sql.strip()

    # Remove markdown code fences
    sql = re.sub(
        r"```(?:sql)?",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "")
    sql = sql.replace("`", "")
    sql = sql.strip()

    if not sql:

        raise ValueError(
            "SQL is empty after cleaning."
        )

    # =====================================================
    # NORMALIZED SQL
    # =====================================================

    upper_sql = sql.upper()

    # Remove trailing semicolon for checking
    check_sql = upper_sql.rstrip(";").strip()

    # =====================================================
    # ONLY ONE SQL STATEMENT
    # =====================================================

    if ";" in check_sql:

        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    # =====================================================
    # ALLOWED STATEMENTS
    # =====================================================

    allowed = (
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE"
    )

    if not check_sql.startswith(allowed):

        raise ValueError(
            "Only SELECT, INSERT, UPDATE and DELETE "
            "queries are allowed."
        )

    # =====================================================
    # BLOCK DANGEROUS COMMANDS
    # =====================================================

    forbidden = [
        "DROP",
        "ALTER",
        "TRUNCATE",
        "PRAGMA",
        "ATTACH",
        "DETACH",
        "VACUUM",
        "REINDEX",
        "CREATE",
    ]

    for keyword in forbidden:

        if re.search(
            rf"\b{keyword}\b",
            upper_sql
        ):

            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )

    # =====================================================
    # UPDATE MUST HAVE WHERE
    # =====================================================

    if re.match(
        r"^\s*UPDATE\b",
        upper_sql
    ):

        if not re.search(
            r"\bWHERE\b",
            upper_sql
        ):

            raise ValueError(
                "UPDATE queries must contain a WHERE clause."
            )

    # =====================================================
    # DELETE MUST HAVE WHERE
    # =====================================================

    if re.match(
        r"^\s*DELETE\b",
        upper_sql
    ):

        if not re.search(
            r"\bWHERE\b",
            upper_sql
        ):

            raise ValueError(
                "DELETE queries must contain a WHERE clause."
            )

    # =====================================================
    # RETURN CLEAN SQL
    # =====================================================

    return sql