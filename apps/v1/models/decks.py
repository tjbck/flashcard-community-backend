from pydantic import BaseModel
from typing import List, Union, Optional
from pymongo import ReturnDocument
import time

from config import DB

####################
# Deck Schema
####################


class DeckModel(BaseModel):
    id: str
    user_id: str

    title: str
    content: str
    group_id: str

    created_at: int  # timestamp in epoch
    updated_at: int
