from pydantic import BaseModel, Field


class AddRequest(BaseModel):
    nums: list[int] = Field(..., description="The numbers to add")
class SubtractRequest(BaseModel):
    nums: list[int] = Field(..., description="The numbers to subtract")
    
class NikhilamNavatashcaramamDashatahRequest(BaseModel):
    multiplicand: int = Field(..., description="The multiplicand")
    multiplier: int = Field(..., description="The multiplier")

class NikhilamNavatashcaramamDashatahResponse(BaseModel):
    multiplicand: int
    multiplier: int
    base: int
    steps: list
    result: int

class EkadhikenaPurvenaRequest(BaseModel):
    number: int = Field(..., description="The number")

class EkadhikenaPurvenaResponse(BaseModel):
    number: int
    steps: list
    result: int

