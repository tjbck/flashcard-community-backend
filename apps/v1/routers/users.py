from fastapi import Response
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import time
import uuid

from apps.v1.models.users import UserModel, Users
from apps.v1.utils.utils import get_session_user


from constants import ERROR_MESSAGES

router = APIRouter()


############################
# GetUsersCount
############################


@router.get("/count", response_model=int)
async def get_users_count():
    return Users.get_num_users()


############################
# GetUsers
############################


@router.get("/", response_model=List[UserModel])
async def get_users(
    skip: int = 0, limit: int = 50, session_user=Depends(get_session_user)
):
    if session_user.role == "admin":
        return Users.get_users({}, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ERROR_MESSAGES.ACCESS_PROHIBITED,
        )
