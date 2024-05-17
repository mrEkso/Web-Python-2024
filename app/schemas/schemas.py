from pydantic import BaseModel, Field, EmailStr


class AccountCreate(BaseModel):
    user_id: int


class Account(BaseModel):
    id: int
    balance: float

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr  # EmailStr is a Pydantic email validation type


class UserCreate(UserBase):
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None, description="New email for the user")
    password: str
    is_admin: bool = False


class User(UserBase):
    id: int
    is_admin: bool
    accounts: list[Account] = []

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: float


class TransactionCreate(TransactionBase):
    account_id: int


class Transaction(TransactionBase):
    id: int
    account: Account

    class Config:
        orm_mode = True
