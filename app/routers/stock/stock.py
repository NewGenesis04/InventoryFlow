import logging
from app.db.schemas import StockUpdate, StockResponse
from fastapi import APIRouter, Depends, HTTPException
from app.db.models import Stock
from sqlalchemy.orm import Session
from app.db.database import get_db 


logger = logging.getLogger(__name__)

router = APIRouter()

