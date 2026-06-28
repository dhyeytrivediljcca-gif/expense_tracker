import os
from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app/expense_tracker.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def seed_demo_data():
    from app.auth import hash_password
    from app.models import Expense, User

    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            demo_user = User(
                name="Student Demo",
                email="student@example.com",
                password=hash_password("Student123"),
            )
            db.add(demo_user)
            db.flush()

            sample_expenses = [
                ("Lunch", 120.0, "Food", date.today(), "Campus lunch"),
                ("Bus Pass", 80.0, "Travel", date.today(), "Monthly pass"),
                ("Groceries", 250.0, "Food", date.today().replace(day=max(1, date.today().day - 2)), "Weekly groceries"),
                ("Books", 450.0, "Education", date.today().replace(day=max(1, date.today().day - 3)), "Course material"),
                ("Movie Night", 300.0, "Entertainment", date.today().replace(day=max(1, date.today().day - 4)), "Weekend outing"),
                ("Coffee", 65.0, "Food", date.today().replace(day=max(1, date.today().day - 5)), "Morning coffee"),
                ("Metro", 40.0, "Travel", date.today().replace(day=max(1, date.today().day - 6)), "Travel card recharge"),
                ("Laptop Charger", 1800.0, "Education", date.today().replace(day=max(1, date.today().day - 7)), "Replacement charger"),
                ("Game Subscription", 199.0, "Entertainment", date.today().replace(day=max(1, date.today().day - 8)), "Monthly subscription"),
            ]

            for title, amount, category, expense_date, note in sample_expenses:
                db.add(
                    Expense(
                        user_id=demo_user.id,
                        title=title,
                        amount=amount,
                        category=category,
                        date=expense_date,
                        note=note,
                        created_at=datetime.utcnow(),
                    )
                )

            db.commit()
    finally:
        db.close()


def init_db():
    create_tables()
    seed_demo_data()
