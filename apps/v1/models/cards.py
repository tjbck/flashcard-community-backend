from pydantic import BaseModel
from typing import List, Union, Optional
from pymongo import ReturnDocument
import time

from config import DB

####################
# Card Schema
####################


class CardModel(BaseModel):
    id: str
    upvotes: int
    downvotes: int
    votes: dict

    title: str
    content: str

    user_id: str
    created_at: int  # timestamp in epoch


####################
# Forms
####################


class CardsTable:
    def __init__(self, db):
        self.db = db
        self.table = db.users

    def insert_new_card(
        self, id: str, username: str, email: str
    ) -> Optional[CardModel]:
        user = CardModel(
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


Cards = CardsTable(DB)
