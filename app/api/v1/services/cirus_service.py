from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.config.settings import get_settings

settings = get_settings()

class CirusService:
    # --- Generic table helpers ---
    async def get_table_data(self, session: AsyncSession, table_name: str) -> List[Dict[str, Any]]:
        """Fetch all rows from a table"""
        try:
            result = await session.execute(text(f"SELECT * FROM `{table_name}`"))
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            print(f"[CirusService] get_table_data error for {table_name}: {e}")
            return []

    async def get_table_data_by_column(self, session: AsyncSession, table_name: str, column: str, value: str) -> List[Dict[str, Any]]:
        """Fetch rows from a table filtered by column value (case-insensitive)"""
        try:
            query = f"SELECT * FROM `{table_name}` WHERE TRIM(LOWER(`{column}`)) = TRIM(LOWER(:value))"
            result = await session.execute(text(query), {"value": value})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            print(f"[CirusService] get_table_data_by_column error for {table_name}: {e}")
            return []

    async def _get_table_columns(self, session: AsyncSession, table_name: str) -> List[str]:
        """Get column names from a table"""
        try:
            result = await session.execute(text(f"SHOW COLUMNS FROM `{table_name}`"))
            cols = [r[0] for r in result.fetchall()]
            return cols
        except Exception as e:
            print(f"[CirusService] _get_table_columns error for {table_name}: {e}")
            return []

    def _find_column(self, cols: List[str], keywords: List[str]) -> Optional[str]:
        """Find a column name matching any of the keywords"""
        for kw in keywords:
            for c in cols:
                if kw.lower() in c.strip().lower():
                    return c
        return None

    async def list_tables(self, session: AsyncSession) -> List[str]:
        """List all tables in the database"""
        try:
            result = await session.execute(text("SHOW TABLES"))
            rows = [r[0] for r in result.fetchall()]
            return rows
        except Exception as e:
            print(f"[CirusService] list_tables error: {e}")
            return []

    async def get_table_schema(self, session: AsyncSession, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a table"""
        try:
            result = await session.execute(text(f"SHOW COLUMNS FROM `{table_name}`"))
            cols = result.fetchall()
            return [dict(row._mapping) for row in cols]
        except Exception as e:
            print(f"[CirusService] get_table_schema error: {e}")
            return []

    async def get_table_rows(self, session: AsyncSession, table_name: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get paginated rows from a table"""
        try:
            if not table_name.replace("_", "").isalnum():
                return []
            query = f"SELECT * FROM `{table_name}` LIMIT :limit OFFSET :offset"
            result = await session.execute(text(query), {"limit": limit, "offset": offset})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            print(f"[CirusService] get_table_rows error: {e}")
            return []

    # --- High-level helpers ---
    async def get_all_continents(self, session: AsyncSession) -> List[Dict[str, Any]]:
        """Get all continents"""
        return await self.get_table_data(session, "continent")

    async def get_all_countries(self, session: AsyncSession) -> List[Dict[str, Any]]:
        """Get all countries ordered by cyber risk rank"""
        try:
            cols = await self._get_table_columns(session, "country")
            rank_col = self._find_column(cols, ["cyber_risk_rank", "cyber_risk", "rank"])
            order_clause = f"ORDER BY `{rank_col}` DESC" if rank_col else ""
            query = f"SELECT * FROM `country` {order_clause}"
            result = await session.execute(text(query))
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            print(f"[CirusService] get_all_countries error: {e}")
            return []

    async def get_countries_by_continent(self, session: AsyncSession, continent: str) -> List[Dict[str, Any]]:
        """Get countries by continent"""
        try:
            cols = await self._get_table_columns(session, "country")
            rank_col = self._find_column(cols, ["cyber_risk_rank", "cyber_risk", "rank"])
            order_clause = f"ORDER BY `{rank_col}` DESC" if rank_col else ""
            query = f"SELECT * FROM `country` WHERE `continent` = :continent {order_clause}"
            result = await session.execute(text(query), {"continent": continent})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            print(f"[CirusService] get_countries_by_continent error: {e}")
            return []

    # --- DHQ-specific helpers ---
    async def get_all_dhq(self, session: AsyncSession) -> List[Dict[str, Any]]:
        """Get all DHQ records"""
        return await self.get_table_data(session, "dhq")

    async def get_dhq_by_state(self, session: AsyncSession, state: str) -> List[Dict[str, Any]]:
        """
        Return all DHQ rows for a given state (state_ut column), case-insensitive,
        ignoring leading/trailing spaces and hidden characters.
        """
        try:
            query = """
            SELECT * FROM dhq
            WHERE TRIM(REPLACE(state_ut, '\\xa0', '')) COLLATE utf8mb4_general_ci = :state
            """
            result = await session.execute(text(query), {"state": state.strip()})
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            print(f"[CirusService] get_dhq_by_state error: {e}")
            return []
