from app.services.base import BaseService
from app.db.models import User, Product, Category, Stock, IncomingOrder, OutgoingOrder, UserRole
from app.db.schemas import DashboardResponse, UserOverview, PerformanceMetrics, RecentActivity, InventoryKPIs, OrderKPIs, UserRoleDistribution
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime, timedelta

class DashboardService(BaseService):
    async def get_dashboard_data(self) -> DashboardResponse:
        user_overview = await self._get_user_overview()
        performance_metrics = await self._get_performance_metrics()
        recent_activity = await self._get_recent_activity()

        return DashboardResponse(
            user_overview=user_overview,
            performance_metrics=performance_metrics,
            recent_activity=recent_activity,
        )

    async def _get_user_overview(self) -> UserOverview:
        total_users_result = await self.db.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar_one()

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        new_users_result = await self.db.execute(
            select(func.count(User.id)).where(User.created_at >= thirty_days_ago)
        )
        new_users_last_30_days = new_users_result.scalar_one()

        roles_result = await self.db.execute(
            select(User.role, func.count(User.id)).group_by(User.role)
        )
        
        role_distribution = {role.name: 0 for role in UserRole}
        for role, count in roles_result:
            role_distribution[role.name] = count

        return UserOverview(
            total_users=total_users,
            new_users_last_30_days=new_users_last_30_days,
            user_role_distribution=UserRoleDistribution(**role_distribution),
        )

    async def _get_performance_metrics(self) -> PerformanceMetrics:
        # Inventory KPIs
        total_products = (await self.db.execute(select(func.count(Product.id)))).scalar_one()
        total_categories = (await self.db.execute(select(func.count(Category.id)))).scalar_one()
        total_stock_quantity = (await self.db.execute(select(func.sum(Stock.available_quantity)))).scalar_one() or 0

        # Inventory Value
        inventory_value_result = await self.db.execute(
            select(func.sum(Stock.available_quantity * Product.price))
            .join(Product, Stock.product_id == Product.id)
        )
        inventory_value = inventory_value_result.scalar_one() or 0.0

        inventory_kpis = InventoryKPIs(
            total_products=total_products,
            total_categories=total_categories,
            total_stock_quantity=total_stock_quantity,
            inventory_value=float(inventory_value)
        )

        # Order KPIs
        total_incoming_orders = (await self.db.execute(select(func.count(IncomingOrder.id)))).scalar_one()
        total_outgoing_orders = (await self.db.execute(select(func.count(OutgoingOrder.id)))).scalar_one()
        total_incoming_value = (await self.db.execute(select(func.sum(IncomingOrder.total_cost)))).scalar_one() or 0.0
        total_outgoing_value = (await self.db.execute(select(func.sum(OutgoingOrder.total_price)))).scalar_one() or 0.0

        order_kpis = OrderKPIs(
            total_incoming_orders=total_incoming_orders,
            total_outgoing_orders=total_outgoing_orders,
            total_incoming_value=float(total_incoming_value),
            total_outgoing_value=float(total_outgoing_value)
        )

        return PerformanceMetrics(inventory=inventory_kpis, orders=order_kpis)

    async def _get_recent_activity(self) -> RecentActivity:
        recent_orders_result = await self.db.execute(
            select(OutgoingOrder).order_by(OutgoingOrder.created_at.desc()).limit(5)
        )
        recent_outgoing_orders = recent_orders_result.scalars().all()

        recent_users_result = await self.db.execute(
            select(User).order_by(User.created_at.desc()).limit(5)
        )
        recent_user_registrations = recent_users_result.scalars().all()

        return RecentActivity(
            recent_outgoing_orders=recent_outgoing_orders,
            recent_user_registrations=recent_user_registrations
        )
