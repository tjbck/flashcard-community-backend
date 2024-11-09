from pydantic import BaseModel
from typing import List, Union, Optional
from pymongo import ReturnDocument
import time

from config import DB

####################
# User DB Schema
####################


class UserModel(BaseModel):
    id: str
    username: str
    email: str
    name: str = ""
    created_at: int  # timestamp in epoch


####################
# Forms
####################


class UserResponse(BaseModel):
    id: str
    username: str
    name: str = ""
    created_at: int  # timestamp in epoch


class UsersTable:
    def __init__(self, db):
        self.db = db
        self.table = db.users

    def insert_new_user(
        self, id: str, username: str, email: str
    ) -> Optional[UserModel]:
        user = UserModel(
            **{
                "id": id,
                "username": username,
                "email": email,
                "created_at": int(time.time()),
            }
        )
        result = self.table.insert_one(user.model_dump())

        if result:
            return user
        else:
            return None

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user = self.table.find_one({"email": email}, {"_id": False})

        if user:
            return UserModel(**user)
        else:
            return None

    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        user = self.table.find_one({"username": username}, {"_id": False})

        if user:
            return UserModel(**user)
        else:
            return None

    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        user = self.table.find_one({"id": id}, {"_id": False})

        if user:
            return UserModel(**user)
        else:
            return None

    def get_users(
        self, filter: dict = {}, skip: int = 0, limit: int = 50
    ) -> List[UserModel]:
        pipeline = [
            {"$match": {**filter}},
            {"$sort": {"createdAt": 1}},
            {"$limit": skip + limit},
            {"$skip": skip},
            {"$project": {"_id": False}},
        ]

        return [
            UserModel(**user)
            for user in list(self.table.aggregate(pipeline, allowDiskUse=True))
        ]

    def get_num_users(self) -> Optional[int]:
        return self.table.count_documents({})

    def update_user_by_id(self, id: str, updated: dict) -> Optional[UserModel]:
        user = self.table.find_one_and_update(
            {"id": id}, {"$set": updated}, return_document=ReturnDocument.AFTER
        )
        return UserModel(**user)


Users = UsersTable(DB)
