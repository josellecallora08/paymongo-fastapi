from pydantic import BaseModel

class PricingPlan(BaseModel):
    name: str
    description: str |  None = None
    price: float
    is_active: bool = True
    max_users: int = 1
    billing_cycle: int = 1
    # e.g., "monthly", "yearly"

class PricingPlanCreate(PricingPlan):
    pass

class PricingPlanOut(PricingPlan):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True
    