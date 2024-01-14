from pydantic import BaseModel
from typing import Optional


class CastIn(BaseModel):

    name: str
    nationality: Optional[str] = None


class CastOut(CastIn):

    id: int


class CastUpdate(BaseModel):

    name: Optional[str] = None
