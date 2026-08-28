from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DbSession, require_user
from app.models import User
from app.schemas.auth import ForgotPasswordRequest, LoginRequest, LogoutRequest, MessageResponse, RefreshRequest, RefreshResponse, SignupRequest, TokenResponse, UserResponse
from app.services.auth import DuplicateEmailError, InvalidCredentialsError, RefreshTokenError, login, refresh, revoke, signup

router = APIRouter(prefix="/auth", tags=["authentication"])


def token_response(user: User, access_token: str, refresh_token: str, expires_at) -> TokenResponse:
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, access_expires_at=expires_at, user=UserResponse.model_validate(user))


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def create_account(payload: SignupRequest, db: DbSession) -> TokenResponse:
    try:
        user, access_token, refresh_token, expires_at = signup(db, payload.full_name, str(payload.email), payload.password)
    except DuplicateEmailError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists") from exc
    return token_response(user, access_token, refresh_token, expires_at)


@router.post("/login", response_model=TokenResponse)
def sign_in(payload: LoginRequest, db: DbSession) -> TokenResponse:
    try:
        user, access_token, refresh_token, expires_at = login(db, str(payload.email), payload.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") from exc
    return token_response(user, access_token, refresh_token, expires_at)


@router.post("/refresh", response_model=RefreshResponse)
def refresh_access_token(payload: RefreshRequest, db: DbSession) -> RefreshResponse:
    try:
        access_token, refresh_token, expires_at = refresh(db, payload.refresh_token)
    except RefreshTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token") from exc
    return RefreshResponse(access_token=access_token, refresh_token=refresh_token, access_expires_at=expires_at)


@router.post("/logout", response_model=MessageResponse)
def sign_out(payload: LogoutRequest, db: DbSession) -> MessageResponse:
    try:
        revoke(db, payload.refresh_token)
    except RefreshTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token") from exc
    return MessageResponse(message="Signed out successfully")


@router.get("/me", response_model=UserResponse)
def get_current_user(user: Annotated[User, Depends(require_user)]) -> UserResponse:
    return UserResponse.model_validate(user)


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(_: ForgotPasswordRequest) -> MessageResponse:
    return MessageResponse(message="Password-reset email is not configured in this environment.")
