from typing import Any

from pydantic import BaseModel, Field


class ExpressionCalculateRequest(BaseModel):
    expression: str = Field(
        ...,
        min_length=1,
        description="Two-number arithmetic expression containing integers and one operator (+, -, *, /)",
        examples=["12+5", "100/4", "-10*25"],
    )


class ExpressionStep(BaseModel):
    step: int
    sutra: str
    details: list[Any] | None = None


class ExpressionCalculateResponse(BaseModel):
    expression: str
    steps: list[ExpressionStep]
