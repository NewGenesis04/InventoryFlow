from fastapi import APIRouter, Depends
from app.db.schemas import DashboardResponse, User
from app.services.dashboard_service import DashboardService
from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.auth_utils import get_current_user, role_required
from app.db.models import UserRole
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_dashboard_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return DashboardService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return DashboardService(db, None)
    
    return _get_service

@router.get("/", response_model=DashboardResponse)
async def get_dashboard_data(
    service: DashboardService = Depends(get_dashboard_service(True)),
    has_permission: bool = Depends(role_required([UserRole.admin, UserRole.staff])),
):
    logger.info("get_dashboard_data endpoint called")
    return await service.get_dashboard_data()
