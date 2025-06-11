from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.pricing_plan import PricingPlan
from app.models.user import User
from app.schemas.pricing_plan import PricingPlanCreate, PricingPlanOut
from app.core.config import settings
import requests
import json

router = APIRouter()
BASE_URL = "https://api.paymongo.com/v1/subscriptions/plans"

@router.post("/create")
def create_pricing_plan(
    plan: PricingPlanCreate,
    db: Session = Depends(get_db)
):
    try:
        existing_plan = db.query(PricingPlan).filter(
            PricingPlan.name == plan.name
        ).first()
        if existing_plan:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pricing plan with this name already exists"
            )
        
        url = "https://api.paymongo.com/v1/subscriptions/plans"

        payload = { "data": { "attributes": {
                    "amount": 2000,
                    "currency": "2",
                    "cycle_count": 1,
                    "description": "s",
                    "interval": "1"
                } } }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Basic {settings.PAYMONGO_TOKEN}"
        }


        response = requests.post(url, json=payload, headers=headers)
        print(f"PayMongo response: {response.text}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create plan on PayMongo: {response.text}"
            )


        new_plan = PricingPlan(**plan.dict())
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        
        return new_plan
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while checking existing plans: {str(e)}"
        )

    

@router.get("/", response_model=list[PricingPlanOut])
def get_pricing_plans(
    db: Session = Depends(get_db),
):
    plans = db.query(PricingPlan).all()
    return plans

@router.get("/{plan_id}", response_model=PricingPlanOut)
def get_pricing_plan(
    plan_id: int,
    db: Session = Depends(get_db),
):
    plan = db.query(PricingPlan).filter(PricingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing plan not found"
        )
    return plan