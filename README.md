# 🚀 SQLPilot AI

> An AI-powered Natural Language to SQL system that lets users query SQLite databases using plain English.

SQLPilot AI converts natural language questions into SQL queries using an AI model, validates the generated SQL for safety, executes it against the selected SQLite database, and displays the results in a conversational interface.

---

## ✨ Features

### 🤖 Natural Language → SQL

- Ask database questions in plain English.
- AI automatically generates the appropriate SQLite query.
- No need to manually write SQL.

### 🗄️ Multiple SQLite Databases

- Upload SQLite `.db` databases.
- Select databases directly from the application.
- Automatically detect available databases and their tables.

### 🧠 Schema-Aware AI

- The selected database schema is read automatically.
- Tables and columns are provided to the AI before SQL generation.
- SQL is generated based on the actual database structure.

### 🔐 SQL Validation

Generated SQL passes through a validation layer before execution.

The system blocks dangerous operations including:

- `DROP`
- `ALTER`
- `TRUNCATE`
- `PRAGMA`
- `ATTACH`
- `DETACH`
- `VACUUM`
- `REINDEX`
- `CREATE`

Additional protection:

- `UPDATE` queries require a `WHERE` clause.
- `DELETE` queries require a `WHERE` clause.
- Multiple SQL statements are rejected.

### ⚡ Automatic Query Execution

- Ask a question and press **Enter**.
- Or click the Generate button.
- SQL is generated, validated, and executed automatically.
- No separate "Execute Query" step is required.

### 💬 Chat-Style Interface

- Conversational database interaction.
- Results appear directly in the conversation.
- Automatically scrolls to the latest response.
- Designed to provide an experience similar to modern AI chat applications.

### 👤 User Authentication

- Login system.
- Create Account functionality.
- Passwords are securely hashed using bcrypt.
- User information is stored in SQLite.

### 🔑 Environment-Based API Key

- OpenRouter API key is loaded from environment variables.
- API keys are not hard-coded into the application.
- `.env` files are excluded from Git.

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
Execute Query
        ↓
Return Results
        ↓
Display Results in Chat


🛠️ Tech Stack
Frontend
React
Vite
JavaScript
Tailwind CSS
Lucide React
Axios
Backend
Python
FastAPI
Uvicorn
SQLite
Pydantic
bcrypt
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
│   │   ├── rule_engine.py
│   │   ├── schema_reader.py
│   │   ├── upload.py
│   │   └── validator.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── CustomButton.jsx
│   │   │   ├── CustomInput.jsx
│   │   │   ├── DatabaseCard.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── LoginCard.jsx
│   │   │   ├── Logo.jsx
│   │   │   └── Sidebar.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   └── Login.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/abhishetty007/sqlpilot-ai.git
cd sqlpilot-ai
🔧 Backend Setup

Go to the backend directory:

cd backend

Create a virtual environment:

python -m venv venv
Activate on Windows

PowerShell:

venv\Scripts\Activate.ps1

Command Prompt:

venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt
🔑 Configure OpenRouter

Create:

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

FastAPI documentation is available at:

http://127.0.0.1:8000/docs
💻 Frontend Setup

Open another terminal.

Go to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
🗃️ Using a Database

SQLPilot AI works with SQLite .db files.

You can upload a database through the application and select it from the database sidebar.

For example:

sakila.db

When a database is selected, SQLPilot automatically reads its tables and columns before sending the schema to the AI.

💬 Example Queries

After selecting a database, you can ask questions such as:

Show all customers
Show the first 10 actors
Show all films
Show customers whose first name is JOHN
Count the number of customers
Show all payments greater than 5

The application will:

Understand the natural language request.
Generate SQL using the database schema.
Validate the generated SQL.
Execute the query.
Display the results directly in the conversation.
🔐 SQL Safety

SQLPilot AI does not blindly execute AI-generated SQL.

Every generated query passes through a validation layer before reaching the database.

Blocked Operations
DROP
ALTER
TRUNCATE
PRAGMA
ATTACH
DETACH
VACUUM
REINDEX
CREATE
Additional Protection
UPDATE requires a WHERE clause.
DELETE requires a WHERE clause.
Multiple SQL statements are rejected.
Only supported SQL statement types are accepted.

This provides an additional safety layer between AI-generated SQL and the database.

👤 Authentication

SQLPilot AI includes a basic authentication system.

Users can:

Create a new account.
Log in with an existing account.
Access the SQL dashboard after authentication.

Passwords are hashed using bcrypt before being stored.

🖥️ User Interface

SQLPilot AI provides a conversational interface designed to make database querying feel similar to chatting with an AI assistant.

The typical workflow is:

Login
  ↓
Select Database
  ↓
Ask a Question
  ↓
Press Enter
  ↓
AI Generates SQL
  ↓
SQL is Validated
  ↓
Query Executes
  ↓
Results Appear in Chat
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

The project combines:

AI + Natural Language Processing + SQL + Database Management + Web Development

into a single application.

👨‍💻 Author

Abhishetty007

GitHub:

https://github.com/abhishetty007

📄 License

This project is intended for educational and development purposes.