from fastapi import APIRouter, HTTPException

from app.schemas.vedic_calculator_schema import (
    ExpressionCalculateRequest,
    ExpressionCalculateResponse,
)
from ..services.vedic_math.vedic_expression_service import VedicExpressionService

router = APIRouter(tags=["vedic-calculator"])
expression_service = VedicExpressionService()


@router.post("/expression-calculate", response_model=ExpressionCalculateResponse)
def expression_calculate(data: ExpressionCalculateRequest):
    try:
        return expression_service.calculate(data.expression)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
