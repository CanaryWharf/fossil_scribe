from typing import List, Optional
from pydantic import BaseModel

class LetterGenRequest(BaseModel):
    concerns: List[str]
    cause: str
    postcode: Optional[str] = None
