from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.databases import get_db
from app.api.v1.services.cirus_service import CirusService

router = APIRouter()
cirus_service = CirusService()

@router.get("/continents")
async def get_continents(session: AsyncSession = Depends(get_db)):
    try:
        data = await cirus_service.get_all_continents(session)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/countries")
async def get_countries(session: AsyncSession = Depends(get_db)):
    try:
        data = await cirus_service.get_all_countries(session)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/countries/{continent}")
async def get_countries_by_continent(continent: str, session: AsyncSession = Depends(get_db)):
    try:
        data = await cirus_service.get_countries_by_continent(session, continent)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/states")
async def get_states(session: AsyncSession = Depends(get_db)):
    try:
        data = await cirus_service.get_table_data(session, "state")
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dhq")
async def get_all_dhq(session: AsyncSession = Depends(get_db)):
    try:
        data = await cirus_service.get_all_dhq(session)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dhq/{state}")
async def get_dhq_by_state(state: str, session: AsyncSession = Depends(get_db)):
    try:
        data = await cirus_service.get_dhq_by_state(session, state)
        if not data:
            print(f"[DEBUG] No DHQ data found for state: {state}")
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tables")
async def get_tables(session: AsyncSession = Depends(get_db)):
    try:
        tables = await cirus_service.list_tables(session)
        return {"success": True, "tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tables/{table_name}/schema")
async def table_schema(table_name: str, session: AsyncSession = Depends(get_db)):
    try:
        schema = await cirus_service.get_table_schema(session, table_name)
        return {"success": True, "schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tables/{table_name}/rows")
async def table_rows(table_name: str, limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_db)):
    try:
        rows = await cirus_service.get_table_rows(session, table_name, limit=limit, offset=offset)
        return {"success": True, "rows": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
