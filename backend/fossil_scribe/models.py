from typing import List
from pydantic import BaseModel

class LetterGenRequest(BaseModel):
    concerns: List[str]
    cause: str
    mp: str
    name: str
