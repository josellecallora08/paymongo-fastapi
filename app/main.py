from fastapi import FastAPI
from app.api.v1 import (auth, plans, webhooks, checkout)
   
app = FastAPI(title="FastAPI Example", description="A simple FastAPI application", version="1.0.0")

    # This function can be used to initialize resources or perform startup tasks
print("Application is starting up...")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(plans.router, prefix="/api/v1/plan", tags=["plan"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])    
app.include_router(checkout.router, prefix="/api/v1/checkout", tags=["checkout"])