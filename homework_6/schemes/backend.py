from typing import List

from pydantic import BaseModel


class ItemList(BaseModel):
    item_ids: List[int]
