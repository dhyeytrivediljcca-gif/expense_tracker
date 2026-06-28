from datetime import date, datetime

from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name is required")
        return value.strip()

    @validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    date: date
    note: str | None = None

    @validator("title")
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title is required")
        return value.strip()

    @validator("amount")
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value

    @validator("category")
    def validate_category(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Category is required")
        return value.strip()


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    title: str
    amount: float
    category: str
    date: date
    note: str | None
    created_at: datetime

    class Config:
        orm_mode = True


class CategorySummary(BaseModel):
    category: str
    total: float


class DashboardSummary(BaseModel):
    total_expense: float
    todays_expense: float
    current_month_expense: float
    expense_by_category: list[CategorySummary]
