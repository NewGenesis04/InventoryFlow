import logging
from app.db.schemas import IncomingOrderCreate, IncomingOrderResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.incoming_orders.service import IncomingOrderService



logger = logging.getLogger(__name__)

def get_incoming_order_service(db: AsyncSession = Depends(get_db)) -> IncomingOrderService:
    return IncomingOrderService(db)

router = APIRouter()

@router.post("/incoming-orders", response_model=IncomingOrderResponse, tatus_code=status.HTTP_201_CREATED)
async def create_incoming_order(order: IncomingOrderCreate, service: IncomingOrderService = Depends(get_incoming_order_service)):
    logger.info(f"Incoming order endpoint accessed")
    try:
        return await service.create_incoming_order(order)
    except Exception as e:
        logger.error(f"Error creating incoming order: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
