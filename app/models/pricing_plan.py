from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.session import Base

class PricingPlan(Base):
    __tablename__ = "pricing_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    max_users = Column(Integer, nullable=False, default=1)
    billing_cycle = Column(String, nullable=False)
    