from fastapi import APIRouter, HTTPException
from typing import List
from app.api.v1.services.melakarta_service import fetch_all_ragas, fetch_raga_by_number
from app.schemas.raga_schema import RagaSchema

router = APIRouter()

@router.get("/melakarta-ragas", response_model=List[RagaSchema])
def get_all_ragas():
    return fetch_all_ragas()

@router.get("/melakarta-ragas/{raga_number}", response_model=RagaSchema)
def get_raga(raga_number: int):
    raga = fetch_raga_by_number(raga_number)
    if not raga:
        raise HTTPException(status_code=404, detail="Raga not found")
    return raga