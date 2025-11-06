from fastapi import HTTPException
from sqlalchemy.future import select
from typing import List
from app.db.models import Category
from app.db.schemas import CategoryCreate, CategoryResponse
from app.services.base import BaseService
import logging
                           
logger = logging.getLogger(__name__)

class CategoryService(BaseService):

    async def create_category(self, category: CategoryCreate) -> CategoryResponse:
        try:
            logger.info(f"Creating a new category with name: {category.name}")
            new_category = Category(**category.model_dump())
            self.db.add(new_category)
            await self.db.commit()
            await self.db.refresh(new_category)
            logger.info(f"Category created successfully with ID: {category.id}")
            return category
        except Exception as e:
            logger.error(f"Error occurred while creating category: {str(e)}")
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        try:
            logger.info(f"Fetching category with ID: {category_id}")
            result = await self.db.execute(select(Category).where(Category.id == category_id))
            category = result.scalars().first()
            if not category:
                logger.error(f"Category with ID {category_id} not found")
                raise HTTPException(status_code=404, detail="Category not found")
            logger.info(f"Category with ID {category_id} fetched successfully")
            return category
        except Exception as e:
            logger.error(f"Error occurred while fetching category: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    async def get_all_categories(self) -> List[CategoryResponse]:
        try:
            logger.info("Fetching all categories")
            result = await self.db.execute(select(Category))
            categories = result.scalars().all()
            logger.info(f"Total categories fetched: {len(categories)}")
            return categories
        except Exception as e:
            logger.error(f"Error occurred while fetching categories: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    async def update_category(self, category_id: int, category_data: CategoryCreate) -> CategoryResponse:
        try:
            logger.info(f"Updating category with ID: {category_id}")
            result = await self.db.execute(select(Category).where(Category.id == category_id))
            category = result.scalars().first()
            if not category:
                logger.error(f"Category with ID {category_id} not found")
                raise HTTPException(status_code=404, detail="Category not found")

            for key, value in category_data.model_dump(exclude_unset=True).items():
                setattr(category, key, value)

            await self.db.commit()
            await self.db.refresh(category)
            logger.info(f"Category with ID {category_id} updated successfully")
            return category
        except Exception as e:
            logger.error(f"Error occurred while updating category: {str(e)}")

            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    async def delete_category(self, category_id: int) :
        try:
            result = await self.db.execute(select(Category).where(Category.id == category_id))
            category = result.scalars().first()       
            if not category:
                logger.error(f"Category with ID {category_id} not found")
                raise HTTPException(status_code=404, detail=f"Category with id ({category_id}) not found")
            self.db.delete(category) 
            await self.db.commit()   

            return {"detail": f"Category with ID ({category_id} has been deleted successfully)"} 

        except Exception as e:
            logger.error(f"Error in deleting category: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
