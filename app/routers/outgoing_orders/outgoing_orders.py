import logging
from app.db.schemas import OutgoingOrderCreate, OutgoingOrderResponse
from app.services.outgoing_order_service import OutgoingOrderService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db 

logger = logging.getLogger(__name__)

router = APIRouter()

async def get_outgoing_order_service(db: Session = Depends(get_db)) -> OutgoingOrderResponse:
    return OutgoingOrderService(db)

@router.post("/outgoing-orders", response_model=OutgoingOrderResponse, status_code=status.HTTP_201_CREATED)
async def outgoing_order(service: OutgoingOrderService = Depends(get_outgoing_order_service), **order: OutgoingOrderCreate):
    logger.info('outgoing-orders route accessed')
    try:
        return await service.created_outgoing_order(order)
    except Exception as e:
        logger.error(f"Error creating outgoing order: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@router.get("/outgoing-orders/{order_id}", response_model=OutgoingOrderResponse)
async def get_outgoing_order(order_id: int, service: OutgoingOrderService = Depends(get_outgoing_order_service)):
    logger.info(f"Fetching outgoing order with ID: {order_id}")
    try:
        return await service.get_outgoing_order(order_id)
    except HTTPException as e:
        logger.error(f"Error fetching outgoing order: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error fetching outgoing order: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")