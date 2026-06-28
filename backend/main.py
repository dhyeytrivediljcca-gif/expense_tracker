from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database import get_db, init_db
from app.models import Expense, User
from app.schemas import DashboardSummary, ExpenseCreate, ExpenseOut, LoginRequest, Token, UserCreate, UserOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() 
    yield


app = FastAPI(title="Student Expense Tracker", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(name=user_data.name, email=user_data.email.lower(), password=hash_password(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email})
    return Token(access_token=token, token_type="bearer", user=UserOut.from_orm(user))


@app.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email.lower()).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})
    return Token(access_token=token, token_type="bearer", user=UserOut.from_orm(user))


@app.get("/expenses", response_model=list[ExpenseOut])
def get_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).order_by(Expense.date.desc(), Expense.created_at.desc()).all()
    return expenses


@app.post("/expenses", response_model=ExpenseOut)
def create_expense(expense_data: ExpenseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    expense = Expense(
        user_id=current_user.id,
        title=expense_data.title,
        amount=expense_data.amount,
        category=expense_data.category,
        date=expense_data.date,
        note=expense_data.note,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@app.get("/expenses/summary", response_model=DashboardSummary)
def expense_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    from datetime import date

    today = date.today()
    current_month = today.month
    current_year = today.year

    total_expense = sum(expense.amount for expense in expenses)
    todays_expense = sum(expense.amount for expense in expenses if expense.date == today)
    current_month_expense = sum(
        expense.amount for expense in expenses if expense.date.month == current_month and expense.date.year == current_year
    )

    grouped: dict[str, float] = {}
    for expense in expenses:
        grouped[expense.category] = grouped.get(expense.category, 0.0) + expense.amount

    summary = [{"category": category, "total": round(total, 2)} for category, total in sorted(grouped.items())]

    return DashboardSummary(
        total_expense=round(total_expense, 2),
        todays_expense=round(todays_expense, 2),
        current_month_expense=round(current_month_expense, 2),
        expense_by_category=summary,
    )


@app.get("/dashboard", response_model=DashboardSummary)
def dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return expense_summary(current_user=current_user, db=db)
