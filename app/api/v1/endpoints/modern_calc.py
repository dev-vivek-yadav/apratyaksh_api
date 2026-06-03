
from fastapi import APIRouter, Depends,HTTPException
from apratyaksh_api.app.api.v1.services.modern_math.modern_expression_service import ModernExpressionService
from apratyaksh_api.app.schemas.modern_calc_schema import modern_calc_request, modern_calc_response

router= APIRouter(tags=["modern-calculator"])

def get_expression_service():
    return ModernExpressionService()

@router.post("/modern-calc",response_model=modern_calc_response)
async def modern_calc(request: modern_calc_request,expression_service:ModernExpressionService = Depends(get_expression_service)):
    try:
        result = expression_service.calculate(request.expression)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    