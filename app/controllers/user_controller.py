from bson import ObjectId
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.schemas import schemas
from app.services import user_service

router = APIRouter()


@router.post("/", response_class=HTMLResponse)
def create_user(user: schemas.UserCreate):
    db_user = user_service.get_user_by_username(user.username)
    if db_user:
        return HTMLResponse(content="<html><body><h1>Error: Username already registered</h1></body></html>",
                            status_code=400)
    new_user = user_service.create_user(user)
    return HTMLResponse(
        content=f"<html><body><h1>User {new_user['username']} successfully created with ID {str(new_user['_id'])}.</h1></body></html>",
        status_code=201)


@router.get("/", response_class=HTMLResponse)
def read_users(request: Request):
    users = user_service.get_users()
    user_list = "<ul>"
    for user in users:
        user_list += f"<li>{user['username']} (ID: {str(user['_id'])} - Admin: {'Yes' if user['is_admin'] else 'No'})</li>"
    user_list += "</ul>"
    return HTMLResponse(content=f"<html><body><h1>List of Users</h1>{user_list}</body></html>")


@router.get("/{user_id}", response_class=HTMLResponse)
def read_user(user_id: str):
    user = user_service.get_user(ObjectId(user_id))
    if not user:
        return HTMLResponse(content="<html><body><h1>Error: User not found</h1></body></html>", status_code=404)
    user_info = (f"<h1>User Details</h1><ul>"
                 f"<li>Username: {user['username']}</li>"
                 f"<li>User ID: {str(user['_id'])}</li>"
                 f"<li>Admin Status: {'Yes' if user['is_admin'] else 'No'}</li>"
                 "</ul>")
    return HTMLResponse(content=f"<html><body>{user_info}</body></html>")


@router.put("/{user_id}", response_class=HTMLResponse)
def update_user(user_id: str, user: schemas.UserUpdate):
    updated_user = user_service.update_user(ObjectId(user_id), user)
    if not updated_user:
        return HTMLResponse(content="<html><body><h1>Error: User not found or no update made.</h1></body></html>",
                            status_code=404)
    return HTMLResponse(
        content=f"<html><body><h1>User {str(updated_user['_id'])} successfully updated.</h1></body></html>")


@router.delete("/{user_id}", response_class=HTMLResponse)
def delete_user(user_id: str):
    deleted_user = user_service.delete_user(ObjectId(user_id))
    if not deleted_user:
        return HTMLResponse(content="<html><body><h1>Error: User not found.</h1></body></html>", status_code=404)
    return HTMLResponse(
        content=f"<html><body><h1>User {str(deleted_user['_id'])} successfully deleted.</h1></body></html>")
