from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from user_models import User
from user_service import (
    register_user_service,
    login_service,
    profile_service,
    update_profile_service
)

from jwt_handler import (
    create_token,
    verify_token
)

from chat_model import ChatRequest
from chat_service import generate_message

router = APIRouter()

@router.post("/register")
def register(user: User):
    register_user_service(user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = login_service(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_token(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/profile")
def profile(payload: dict = Depends(verify_token)):
    user = profile_service(payload["sub"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "username": user["username"],
        "email": user["email"],
        "date_of_birth": user["date_of_birth"]
    }

@router.put("/update-profile")
def update_profile(
    user: User,
    payload: dict = Depends(verify_token)
):
    result = update_profile_service(
        payload["sub"],
        {
            "email": user.email,
            "password": user.password,
            "date_of_birth": user.date_of_birth
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"message": "Updated"}

@router.post("/chat")
def chat(
    request: ChatRequest,
    payload: dict = Depends(verify_token)
):
    response = generate_message(request.messages)

    return {
        "message": response
    }