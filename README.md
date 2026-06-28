# Student Expense Tracker

A simple full-stack expense tracking MVP for students built with FastAPI, React, Vite, Tailwind CSS, SQLAlchemy, and JWT authentication.

## Features
- User registration and login
- Protected dashboard routes
- Add and view expenses
- Dashboard summaries and charts
- SQLite database with demo account

## Demo Account
- Email: student@example.com
- Password: Student123

## Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment
Copy [.env.example](.env.example) to .env and adjust values if needed.
