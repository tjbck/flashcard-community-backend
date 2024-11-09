from pydantic import BaseModel
from typing import List, Union, Optional
import time
import uuid

from apps.v1.models.users import UserModel, Users
from apps.v1.utils.utils import verify_password

import config

DB = config.DB

####################
# Auth MODEL
####################


class AuthModel(BaseModel):
    id: str
    email: str
    password: str
    active: bool = True


####################
# Forms
####################


class Token(BaseModel):
    token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str


class SigninResponse(Token, UserResponse):
    pass


class SigninForm(BaseModel):
    email: str
    password: str


class SignupForm(BaseModel):
    username: str
    email: str
    password: str


class AuthsTable:
    def __init__(self, db):
        self.db = db
        self.table = db.auths

    def insert_new_auth(
        self, email: str, password: str, username: str
    ) -> Optional[UserModel]:
        id = str(uuid.uuid4())

        auth = AuthModel(
            **{"id": id, "email": email.lower(), "password": password, "active": True}
        )
        result = self.table.insert_one(auth.model_dump())
        user = Users.insert_new_user(id, username.lower(), email.lower())

        print(result, user)
        if result and user:
            return user
        else:
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        auth = self.table.find_one({"email": email, "active": True})

        if auth:
            if verify_password(password, auth["password"]):
                user = self.db.users.find_one({"id": auth["id"]})
                return UserModel(**user)
            else:
                return None
        else:
            return None


Auths = AuthsTable(DB)
