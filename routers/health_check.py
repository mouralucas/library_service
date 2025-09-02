from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session

router = APIRouter(prefix="/health-check", tags=["Health Check"])


@router.get(
    "/service",
    description="Health check endpoint to verify if the service is running",
)
async def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return {"status": "ok", "message": "Service is running"}


@router.get(
    "/database", description="Health check endpoint to verify database connectivity"
)
async def database_health_check(session: AsyncSession = Depends(get_session)):
    """
    Health check endpoint to verify database connectivity.
    """
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database is reachable"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )
