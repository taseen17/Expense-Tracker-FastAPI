# Expense Tracker API

A REST API for tracking personal expenses, built with **FastAPI**, **SQLAlchemy** and **PostgreSQL**. Database schema changes are managed with **Alembic** migrations, and the endpoints are covered by **pytest** tests.

## Features

- Create, read, update and delete expenses
- Categories for expenses, e.g. food, transport, bills
- Filter expenses by date range / category
- User registration and JWT authentication
- Request validation with Pydantic and clear error responses
- Interactive API docs generated automatically (Swagger UI / OpenAPI)

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.[x] |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Testing | pytest |

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI app and router setup
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # DB engine and session
│   └── routers/         # API route modules
├── alembic/             # Migration scripts
├── tests/               # pytest tests
├── alembic.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/taseen17/https://github.com/taseen17/Expense-Tracker-FastAPI.git
cd Expense-Tracker-FastAPI
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/expense_tracker
[SECRET_KEY=your-secret-key]
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

The API is now running at `http://127.0.0.1:8000`.

## API Documentation

FastAPI generates interactive documentation automatically:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Example Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/expenses` | Create a new expense |
| GET | `/expenses` | List expenses |
| GET | `/expenses/{id}` | Get a single expense |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |

> Replace with your actual routes.

## Running Tests

```bash
pytest
```

## Database Migrations

Create a new migration after changing a model:

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

## Author

**Mir Muktadir Ali Taseen**
GitHub: (https://github.com/taseen17)
LinkedIn: (https://linkedin.com/in/mir-muktadir-ali-taseen-68098a2a4)
