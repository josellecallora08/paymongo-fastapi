from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from app.db.session import get_db
import requests
from app.schemas.webhook import WebhookCreate
from app.core.config import Settings

router = APIRouter()

# Handle incoming webhooks from PayMongo
@router.post("/payment-webhooks")
async def handle_webhook(request: Request, db=Depends(get_db)):
    try:
        # Get the raw body
        body = await request.body()
        print(f"Received webhook body: {body.decode('utf-8')}")
        
        # Parse the JSON data
        webhook_data = await request.json()
        
        # Extract payment information
        event_type = webhook_data["data"]["attributes"]["type"]
        payment_data = webhook_data["data"]["attributes"]["data"]
        
        if event_type == "payment.paid":
            # Handle successful payment
            payment_id = payment_data["id"]
            amount = payment_data["attributes"]["amount"]
            status = payment_data["attributes"]["status"]
            customer_email = payment_data["attributes"]["billing"]["email"]
            
            print(f"Payment successful: {payment_id}, Amount: {amount}, Email: {customer_email}")
            
            try:
                # Here you can add your logic to handle the payment, e.g., update database, send email, etc.
                # Example: await update_payment_status(db, payment_id, status)
                pass

            except Exception as e:
                print(f"Error processing payment: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error while processing payment")
        
        # Return JSON response (FastAPI way)
        return JSONResponse(
            content={
                "status": "success", 
                "message": "Webhook received successfully"
            },
            status_code=200
        )
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")

# Create a webhook for payment events
@router.post("/create-webhook")
def create_webhook(form_data: WebhookCreate, db = Depends(get_db)):
    url = "https://api.paymongo.com/v1/webhooks"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}"
    }
    payload = {
        "data": {
            "attributes": {
                "url": form_data.url,
                "events": form_data.events if form_data.events else [],
            }
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500,
            detail=f"Webhook creation failed: {str(e)}"
        )

    return {"message": "Webhook created successfully", "status": "success"}

# Retrieve all webhook events
@router.get("/webhook-events")
def get_webhook_events(db=Depends(get_db)):
    url = "https://api.paymongo.com/v1/webhooks"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500,
            detail=f"Failed to retrieve webhook events: {str(e)}"
        )

    return response.json()

# Retrieve a specific webhook event by ID
@router.get("/webhook-event/{webhook_id}")
def get_webhook_event(webhook_id: str, db=Depends(get_db)):
    url = f"https://api.paymongo.com/v1/webhooks/{webhook_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500,
            detail=f"Failed to retrieve webhook event: {str(e)}"
        )

    return response.json()

# Disable a webhook event
@router.post("/webhook-event/{webhook_id}")
def disable_webhook_event(webhook_id: str, db=Depends(get_db)):
    url = f"https://api.paymongo.com/v1/webhooks/{webhook_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500,
            detail=f"Failed to disable webhook event: {str(e)}"
        )

    return {"message": "Webhook event disabled successfully", "status": "success"}

# Enable a webhook event
@router.put("/webhook-event/{webhook_id}/enable")
def enable_webhook_event(webhook_id: str, db=Depends(get_db)):
    url = f"https://api.paymongo.com/v1/webhooks/{webhook_id}/enable"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}"
    }
    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500,
            detail=f"Failed to enable webhook event: {str(e)}"
        )
    return {"message": "Webhook event enabled successfully", "status": "success"}

# Update a webhook event
@router.put("/webhook-event/{webhook_id}")
def update_webhook_event(webhook_id: str, form_data: WebhookCreate, db=Depends(get_db)):
    url = f"https://api.paymongo.com/v1/webhooks/{webhook_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}"
    }
    payload = {
        "data": {
            "attributes": {
                "url": form_data.url,
                "events": form_data.events if form_data.events else [],
            }
        }
    }

    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=response.status_code if response else 500,
            detail=f"Webhook update failed: {str(e)}"
        )

    return {"message": "Webhook updated successfully", "status": "success"}

