from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas import schemas
from app.services import user_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_class=HTMLResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        return HTMLResponse(content="<html><body><h1>Error: Username already registered</h1></body></html>",
                            status_code=400)
    new_user = user_service.create_user(db=db, user=user)
    return HTMLResponse(
        content=f"<html><body><h1>User {new_user.username} successfully created with ID {new_user.id}.</h1></body></html>",
        status_code=201)


@router.get("/", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_db)):
    users = user_service.get_users(db)
    user_list = "<ul>"
    for user in users:
        username = user.username
        user_id = user.id
        is_admin = 'Yes' if user.is_admin else 'No'
        user_list += f"<li>{username} (ID: {user_id} - Admin: {is_admin})</li>"
    user_list += "</ul>"
    return HTMLResponse(content=f"<html><body><h1>List of Users</h1>{user_list}</body></html>")


@router.get("/{user_id}", response_class=HTMLResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id=user_id)
    if user is None:
        return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
    user_info = (
        f"<h1>User Details</h1><ul>"
        f"<li>Username: {user.username}</li>"
        f"<li>User ID: {user.id}</li>"
        f"<li>Admin Status: {'Yes' if user.is_admin else 'No'}</li>"
        "</ul>"
    )
    return HTMLResponse(content=f"<html><body>{user_info}</body></html>")


@router.put("/{user_id}", response_class=HTMLResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_service.update_user(db, user_id=user_id, user=user)
    if updated_user is None:
        return HTMLResponse(content="<html><body><h1>Error: User not found or no update made.</h1></body></html>",
                            status_code=404)
    return HTMLResponse(content=f"<html><body><h1>User {updated_user.id} successfully updated.</h1></body></html>")


@router.delete("/{user_id}", response_class=HTMLResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = user_service.delete_user(db, user_id=user_id)
    if deleted_user is None:
        return HTMLResponse(content="<html><body><h1>Error: User not found.</h1></body></html>", status_code=404)
    return HTMLResponse(content=f"<html><body><h1>User {deleted_user.id} successfully deleted.</h1></body></html>")
