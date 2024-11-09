from pydantic import BaseModel
from typing import List, Union, Optional
from pymongo import ReturnDocument
import time

from config import DB

####################
# Group Schema
####################


class GroupModel(BaseModel):
    id: str

    name: str
    prompt: str

    admin_ids: List[str]

    created_at: int  # timestamp in epoch
    updated_at: int
