from fastapi import APIRouter,Request
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from ..services.ganita_service import GanitaService
from app.schemas.ganita_schema import *


router = APIRouter()
ganita_service = GanitaService()


@router.post("/add")
def ganita(data:AddRequest):
    return ganita_service.add(data.nums)
    
@router.post("/subtract")
def ganita(data:SubtractRequest):
    return ganita_service.subtract(data.nums)


@router.post("/urdhva-tiryagbhyam")
def ganita(a: int, b: int):
    return ganita_service.urdhva_tiryagbhyam(a, b)

@router.post("/ekadhikena-purvena")
def ganita(n: int):
    return ganita_service.ekadhikena_purvena(n)

@router.post("/nikhilam-navatashcaramam-dashatah")
def ganita(a: int, b: int):
    return ganita_service.nikhilam_navatashcaramam_dashatah(a, b)

@router.post("/multiplication")
def multiplication(a:int, b:int):
    return ganita_service.multiplication(a,b)


