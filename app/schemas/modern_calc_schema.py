
from typing import Any
from pydantic import BaseModel,Field


class modern_calc_request(BaseModel):
    expression: str = Field(..., description="The arithmetic expression to evaluate, e.g., '2 + 3 * 4'")


class modern_calc_response(BaseModel):
    operation:str
    steps:list[Any]
    result:float | int







