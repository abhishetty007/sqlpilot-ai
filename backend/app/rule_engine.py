import re


# =========================================================
# STUDENTS DATABASE RULES
# =========================================================

def _students(text):

    # ------------------------------
    # SHOW ALL
    # ------------------------------
    if any(x in text for x in [
        "all students",
        "show students",
        "show all",
        "display students",
        "list students"
    ]):
        return "SELECT * FROM students;"

    # ------------------------------
    # TOPPER / BEST / SMARTEST
    # ------------------------------
    if any(x in text for x in [
        "topper",
        "best student",
        "smartest student",
        "highest marks",
        "highest scorer",
        "top student"
    ]):
        return "SELECT * FROM students ORDER BY marks DESC LIMIT 1;"

    # ------------------------------
    # WEAK / FAILED STUDENTS
    # ------------------------------
    if any(x in text for x in [
        "weak students",
        "failed students",
        "fail students",
        "students who failed",
        "low scorers"
    ]):
        return "SELECT * FROM students WHERE marks < 40;"

    # ------------------------------
    # ABOVE MARKS
    # ------------------------------
    match = re.search(r"(above|more than|greater than)\s+(\d+)", text)

    if match:
        marks = match.group(2)
        return f"SELECT * FROM students WHERE marks > {marks};"

    # ------------------------------
    # BELOW MARKS
    # ------------------------------
    match = re.search(r"(below|less than)\s+(\d+)", text)

    if match:
        marks = match.group(2)
        return f"SELECT * FROM students WHERE marks < {marks};"

    # ------------------------------
    # EXACT MARKS
    # ------------------------------
    match = re.search(r"marks\s+(\d+)", text)

    if match:
        marks = match.group(1)
        return f"SELECT * FROM students WHERE marks = {marks};"

    # ------------------------------
    # STUDENT BY ID
    # ------------------------------
    match = re.search(r"id\s+(\d+)", text)

    if match:
        sid = match.group(1)
        return f"SELECT * FROM students WHERE id = {sid};"

    # ------------------------------
    # STUDENT NAME QUERY
    # ------------------------------
    names = [
        "abhinandan",
        "abhishek",
        "rahul",
        "riya",
        "priya",
        "divya",
        "arjun",
        "rohit",
        "sneha",
        "kiran",
        "lokesh",
        "aman",
        "loki"
    ]

    for name in names:
        if name in text:
            return f"SELECT * FROM students WHERE LOWER(name) LIKE '%{name}%';"

    # ------------------------------
    # COUNT
    # ------------------------------
    if "count" in text:
        return "SELECT COUNT(*) AS total_students FROM students;"

    # ------------------------------
    # AVERAGE
    # ------------------------------
    if any(x in text for x in [
        "average",
        "avg marks",
        "mean marks"
    ]):
        return "SELECT AVG(marks) AS average_marks FROM students;"

    return None


# =========================================================
# LIBRARY DATABASE RULES
# =========================================================

def _library(text):

    # SHOW ALL BOOKS
    if any(x in text for x in [
        "all books",
        "show books",
        "list books",
        "display books"
    ]):
        return "SELECT * FROM books;"

    # AVAILABLE BOOKS
    if any(x in text for x in [
        "available books",
        "books available",
        "free books"
    ]):
        return "SELECT * FROM books WHERE available = 1;"

    # UNAVAILABLE BOOKS
    if any(x in text for x in [
        "unavailable books",
        "issued books",
        "checked out books"
    ]):
        return "SELECT * FROM books WHERE available = 0;"

    # AUTHOR SEARCH
    authors = [
        "paulo coelho",
        "stephen hawking",
        "james clear",
        "george orwell",
        "robert c martin"
    ]

    for author in authors:
        if author in text:
            return f"SELECT * FROM books WHERE LOWER(author) LIKE '%{author}%';"

    return None


# =========================================================
# HOSPITAL DATABASE RULES
# =========================================================

def _hospital(text):

    # SHOW ALL PATIENTS
    if any(x in text for x in [
        "all patients",
        "show patients",
        "list patients"
    ]):
        return "SELECT * FROM patients;"

    # DIABETES PATIENTS
    if "diabetes" in text:
        return "SELECT * FROM patients WHERE LOWER(disease) = 'diabetes';"

    # DOCTOR SEARCH
    doctors = [
        "dr. sharma",
        "dr. mehta",
        "dr. rao"
    ]

    for doctor in doctors:
        if doctor in text:
            return f"SELECT * FROM patients WHERE LOWER(doctor) LIKE '%{doctor}%';"

    return None


# =========================================================
# MAIN RULE ENGINE
# =========================================================

def nl_to_sql_rule(user_input, db_name):

    text = user_input.lower().strip()

    if "student" in db_name.lower():

        return _students(text)

    elif "library" in db_name.lower():

        return _library(text)

    elif "hospital" in db_name.lower():

        return _hospital(text)

    return None