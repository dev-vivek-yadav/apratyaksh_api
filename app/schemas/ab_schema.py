from pydantic import BaseModel
from typing import Optional, List, Any


class ProcessWordRequest(BaseModel):
    word: str
    inputScript: str = "latin"


class CalculateRequest(BaseModel):
    tokens: List[Any]
    operation: str



class AddMappingRequest(BaseModel):
    number: int
    latinChar: str
    devanagariChar: Optional[str] = None 
    kannadaChar: Optional[str] = None
    # tamilChar: Optional[str] = None  # Commented Tamil support
    teluguChar: Optional[str] = None
    type: str
    colorHex: Optional[str] = None
