# v1 router
# app/api/v1/router.py
from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.aryabhatta import router as aryabhatta_router
from .endpoints.ganita import router as ganita_router
from .endpoints import ragas,  cirus

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(aryabhatta_router, prefix="/aryabhatta")
router.include_router(ganita_router, prefix="/ganita")
router.include_router(ragas.router, prefix="/melakarta", tags=["melakarta"])
router.include_router(cirus.router, prefix="/cirus", tags=["cirus"])
