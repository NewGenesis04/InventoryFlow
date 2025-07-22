from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from typing import List
from app.db.models import Product, Stock
from app.db.schemas import ProductCreate, ProductResponse, ProductUpdate, ProductSummary
from app.services.base import BaseService
from sqlalchemy.orm import selectinload
import logging

logger = logging.getLogger(__name__)


class ProductService(BaseService):

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        try:

            result = await self.db.execute(select(Product).where(Product.name == product.name))
            existing_product = result.scalars().first()
            if existing_product:
                logger.warning(f"Product with name {product.name} already exists")
                raise HTTPException(status_code=400, detail="")
            
            new_product = Product(**product.model_dump())
            self.db.add(new_product)
            await self.db.commit()
            await self.db.refresh(new_product)

            return ProductResponse.model_validate(new_product)

        except Exception as e:
            logger.error(f"Product could not be created because of error: {str(e)}")
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Error in creating product")
        
    async def get_product_by_id(self, id: int) -> ProductResponse:
        try:
            result = await self.db.execute(
                select(Product)
                .options(selectinload(Product.category))
                .where(Product.id == id)
            )
            product = result.scalars().first()
            if not product:
                logger.warning(f"No product with id ({id}) found in database")
                raise HTTPException(status_code=400, detail=f"No products with id ({id}) found")
            logger.info(f"Product with ID ({product.id}) fetched succesfully")
            return ProductResponse.model_validate(product)

        except Exception as e:
            logger.error(f"Product could not be fetched due to error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    async def get_all_products(self) -> List[ProductSummary]:
        try:
            result = await self.db.execute(select(Product))
            products = result.scalars().all()
            if not products:
                logger.warning("No products found in database")
                raise HTTPException(status_code=400, detail="No products found")
            

            logger.info(f"Total products returned: {len(products)}")
            return products

        except Exception as e:
            logger.error(f"Error in fetching products: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    async def update_product(self, id: int, product_update: ProductUpdate) -> ProductResponse:
        try:
            result = await self.db.execute(select(Product).options(selectinload(Product.category)).where(Product.id == id))
            product = result.scalars().first()
            if not product:
                logger.warning(f"No product with id ({id}) found in database")
                raise HTTPException(status_code=400, detail=f"No products with id ({id}) found")
            
            for key, value in product_update.model_dump(exclude_unset=True).items():
                setattr(product, key, value)
            
            await self.db.commit()
            await self.db.refresh(product)

            logger.info(f"Product with ID ({id} updated succesfully)")

            return ProductResponse.model_validate(product)


        except Exception as e:
            logger.error(f"Error occurred while updating product: {str(e)}")
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")
        

    async def delete_product(self, id: int) -> str:
        try:
            result = await self.db.execute(select(Product).where(Product.id == id))
            product = result.scalars().first()
            if not product:
                logger.warning(f"No product with id ({id}) found in database")
                raise HTTPException(status_code=400, detail=f"No products with id ({id}) found")
            
            self.db.delete(product)
            await self.db.commit()

            return {"detail": f"Product with ID ({id}) has been deleted successfully"}

            
        except Exception as e:
            logger.error(f"Error deleting product with id ({id}) from database: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")