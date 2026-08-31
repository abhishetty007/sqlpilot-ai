# 🚀 SQLPilot AI

> An AI-powered Natural Language to SQL system that lets users query SQLite databases using plain English.

SQLPilot AI converts natural language questions into SQL queries using an AI model, validates the generated SQL for safety, executes it against the selected SQLite database, and displays the results in a conversational interface.

---

## ✨ Features

- 🤖 **Natural Language → SQL**
  - Ask database questions in plain English.
  - AI automatically generates the appropriate SQLite query.

- 🗄️ **Multiple SQLite Databases**
  - Upload and select `.db` databases.
  - Automatically detect available databases and their tables.

- 🧠 **Schema-Aware AI**
  - The database schema is provided to the AI before generating SQL.
  - Queries are generated using the available tables and columns.

- 🔐 **SQL Validation**
  - Generated SQL is validated before execution.
  - Dangerous operations such as `DROP`, `ALTER`, `TRUNCATE`, `PRAGMA`, `ATTACH`, and `DETACH` are blocked.
  - `UPDATE` and `DELETE` queries require a `WHERE` clause.
  - Multiple SQL statements are rejected.

- ⚡ **Automatic Query Execution**
  - No need to generate SQL and then manually execute it.
  - Press **Enter** or click Generate to process the request.

- 💬 **Chat-Style Interface**
  - Conversational database interaction.
  - Automatically scrolls to the latest response.
  - Results are displayed directly in the conversation.

- 🔑 **Secure API Key Handling**
  - OpenRouter API key is loaded through environment variables.
  - `.env` files are excluded from Git.

- 👤 **User Authentication**
  - Login system for accessing the application.

---

## 🧠 How It Works

```text
User asks a question
        ↓
Frontend sends request
        ↓
FastAPI Backend
        ↓
Read selected database schema
        ↓
OpenRouter AI
        ↓
Generate SQLite SQL
        ↓
SQL Validation
        ↓
Execute query
        ↓
Return results
        ↓
Display results in chat

🛠️ Tech Stack
Frontend
React
Vite
Tailwind CSS
JavaScript
Lucide React
Backend
Python
FastAPI
Uvicorn
SQLite
Pydantic
AI
OpenRouter API
AI-powered Natural Language → SQL generation



📁 Project Structure
NL_TO_SQL_V2/
│
├── backend/
│   ├── app/
│   │   ├── ai_engine.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── query_executor.py
│   │   ├── schema_reader.py
│   │   ├── upload.py
│   │   └── validator.py
│   │
│   ├── uploaded_databases/
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── DatabaseCard.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── LoginCard.jsx
│   │   │   └── Sidebar.jsx
│   │   │
│   │   └── pages/
│   │       └── Dashboard.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md



⚙️ Installation
1. Clone the repository
git clone https://github.com/abhishetty007/sqlpilot-ai.git
cd sqlpilot-ai
🔧 Backend Setup

Go to the backend directory:

cd backend

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
🔑 Configure OpenRouter

Create a file:

backend/.env

Add:

OPENROUTER_API_KEY=your_api_key_here

Replace your_api_key_here with your OpenRouter API key.

Never commit your .env file or API key to GitHub.

▶️ Start the Backend

From the backend directory:

python -m uvicorn app.main:app --reload

The backend will run at:

http://127.0.0.1:8000
💻 Frontend Setup

Open another terminal and go to:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
🗃️ Using a Database

SQLPilot works with SQLite .db files.

You can upload a database through the application and then select it from the database sidebar.

For example, using the Sakila database:

sakila.db

SQLPilot automatically reads its tables and columns before sending the schema to the AI.

💬 Example Queries

Once a database is selected, you can ask questions such as:

Show all customers
Show the first 10 actors
Show all films
Show customers whose first name is JOHN
Count the number of customers
Show all payments greater than 5

The system generates the corresponding SQL, validates it, executes it, and displays the results.

🔐 SQL Safety

SQLPilot does not blindly execute AI-generated SQL.

Before execution, queries pass through a validation layer.

Blocked operations
DROP
ALTER
TRUNCATE
PRAGMA
ATTACH
DETACH
VACUUM
REINDEX
CREATE
Additional protection

UPDATE and DELETE statements must contain a WHERE clause.

Multiple SQL statements are also rejected.

This provides an additional safety layer between the AI-generated query and the database.

🖥️ User Interface

SQLPilot provides a conversational interface designed to make database querying feel similar to chatting with an AI assistant.

The user can:

Log in.
Select a database.
Ask a question.
Press Enter or generate the query.
Receive the database results directly in the conversation.
🔮 Future Improvements

Possible future versions could include:

🔵 Google OAuth login
📊 Automatic charts and visualizations
🧠 Improved SQL generation models
💾 Query history and saved queries
📤 Export results to CSV/Excel
🔍 Advanced database search
👥 User-specific database management
☁️ Cloud deployment
🐳 Docker support
📈 Query performance analysis
🎯 Project Goal

The goal of SQLPilot AI is to make SQL databases easier to interact with by allowing users to communicate with their data using natural language instead of manually writing SQL queries.

It combines:

AI + Natural Language Processing + SQL + Database Management + Web Development

into a single application.

👨‍💻 Author

Abhishetty007

GitHub:

https://github.com/abhishetty007

📄 License

This project is intended for educational and development purposes.


