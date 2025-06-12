from pydantic import BaseModel
from typing import Optional

class CheckoutSession(BaseModel):
    amount: float
    description: Optional[str] = None
    quantity: Optional[int] = 1
    name: Optional[str] = "Sample Item"

    class Config:
        from_attributes = True
        