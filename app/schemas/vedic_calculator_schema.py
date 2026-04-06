from typing import Any

from pydantic import BaseModel, Field


class ExpressionCalculateRequest(BaseModel):
    expression: str = Field(
        ...,
        min_length=1,
        description="Arithmetic expression containing integers and +, -, *, / operators",
        examples=["12+5*3-9", "100/4+25*2-3", "-10+25*4-3/2+9"],
    )


class ExpressionStep(BaseModel):
    step: int
    sutra: str
    operation: str
    before: str
    after: str
    explanation: str
    result_after_step: float | int
    details: list[Any] | None = None


class ExpressionCalculateResponse(BaseModel):
    expression: str
    normalized_expression: str
    result: float | int
    steps: list[ExpressionStep]
