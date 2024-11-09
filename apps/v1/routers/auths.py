from fastapi import Response
from fastapi import Cookie
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Union

from fastapi import APIRouter
from pydantic import BaseModel
import time
import uuid

from apps.v1.models.auths import (
    SigninForm,
    SignupForm,
    UserResponse,
    SigninResponse,
    Auths,
)
from apps.v1.models.users import Users

from apps.v1.utils.utils import get_password_hash, create_token, get_session_user
from constants import ERROR_MESSAGES

from config import ENV


router = APIRouter()

############################
# GetSessionUser
############################


@router.get("/", response_model=UserResponse)
async def get_current_session_user(session_user=Depends(get_session_user)):

    return {
        "id": session_user.id,
        "email": session_user.email,
        "username": session_user.username,
        "profileImageUrl": session_user.profileImageUrl,
    }


@router.get("/cookie", response_model=UserResponse)
async def get_session_user(session_user=Depends(get_session_user)):
    return {
        "id": session_user.id,
        "email": session_user.email,
        "username": session_user.username,
        "profileImageUrl": session_user.profileImageUrl,
    }


############################
# SignOut
############################


@router.get("/signout")
async def signout(response: Response):
    response.set_cookie(
        key="token",
        value="",
        samesite="None",
        httponly=True,
        secure=True,
    )
    return {"status": True}


############################
# SignIn
############################


@router.post("/signin", response_model=SigninResponse)
async def signin(response: Response, form_data: SigninForm):
    user = Auths.authenticate_user(form_data.email.lower(), form_data.password)
    if user:
        token = create_token(data={"email": user.email})
        response.set_cookie(
            key="token",
            value=token,
            samesite="None",
            httponly=True,
            secure=True,
        )

        return {
            "token": token,
            "token_type": "Bearer",
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "profileImageUrl": user.profileImageUrl,
        }
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)


############################
# SignUp
############################


@router.post("/signup", response_model=SigninResponse)
async def signup(response: Response, form_data: SignupForm):
    if not Users.get_user_by_email(form_data.email.lower()):
        if not Users.get_user_by_username(form_data.username.lower()):
            try:
                hashed = get_password_hash(form_data.password)
                user = Auths.insert_new_auth(
                    form_data.email.lower(), hashed, form_data.username.lower()
                )

                if user:
                    token = create_token(data={"email": user.email})
                    response.set_cookie(
                        key="token",
                        value=token,
                        samesite="None",
                        httponly=True,
                        secure=True,
                    )

                    return {
                        "token": token,
                        "token_type": "Bearer",
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "profileImageUrl": user.profileImageUrl,
                    }
                else:
                    raise HTTPException(500, detail=ERROR_MESSAGES.DEFAULT())
            except Exception as err:
                raise HTTPException(500, detail=ERROR_MESSAGES.DEFAULT(err))
        else:
            raise HTTPException(400, detail=ERROR_MESSAGES.USERNAME_TAKEN)
    else:
        raise HTTPException(400, detail=ERROR_MESSAGES.EMAIL_TAKEN)
