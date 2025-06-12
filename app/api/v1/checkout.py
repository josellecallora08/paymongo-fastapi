from fastapi import APIRouter, HTTPException, status, Depends
from app.core.config import settings as Settings
import requests
from uuid import uuid4
from app.schemas.checkout import CheckoutSession
router = APIRouter()
BASE_URL = "https://api.paymongo.com/v1/checkout_sessions"

@router.post("/create")
def create_checkout_session(form_data: CheckoutSession):
    """
    Create a checkout session for the user.
    This endpoint is used to initiate a payment process.
    """
    url = f"{BASE_URL}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}",
        "accept": "application/json"
    }
    payload = {
    "data": {
        "attributes": {
        "send_email_receipt": False,
        "show_description": True,
        "show_line_items": True,
        "line_items": [
            {
            "currency": "PHP",
            "amount": int(form_data.amount * 100),  # Convert to cents
            "name": form_data.name,
            "quantity": int(form_data.quantity),
            "description": form_data.description
            }
        ],
        "payment_method_types": [
            "gcash",
            "paymaya",
            "grab_pay",
            "card",
            "qrph"
        ],
        "description": "Test Checkout",
        "reference_number": f"Ref-{uuid4().hex[:10]}",  # Replace with a unique reference number
        "success_url": "https://example.com/success", # Replace with your success URL
        "cancel_url": "https://example.com/cancel", # Replace with your cancel URL
        "statement_descriptor": "Test Payment",
        }
    }
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        status = response.raise_for_status()
        print(f"Response status code: {response.status_code}")

        if response.status_code is 200:
            print(f"Response status: {status}")

            ## Check if the response is valid JSON
            try:
                response_data = response.json()
                print(f"Response data: {response_data}")

                # Handle the response data as needed



            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Invalid JSON response from payment gateway"
                )


        return {"message": "Checkout session created successfully", "response": response.json()}
    
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "error": str(http_err),
                "response": response.json()  # Or response.json() if you're confident it's valid JSON
            }
        )


@router.get("/retrieve/{session_id}")
def retrieve_checkout_session(session_id: str):
    """
    Retrieve a checkout session by its ID.
    This endpoint is used to get the details of a specific checkout session.
    """
    url = f"{BASE_URL}/{session_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}",
        "accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "error": str(http_err),
                "response": response.json()  # Or response.json() if you're confident it's valid JSON
            }
        )
    

@router.post("/expire/{session_id}")
def expire_checkout_session(session_id: str):
    """
    Expire a checkout session by its ID.
    This endpoint is used to mark a checkout session as expired.
    """
    url = f"{BASE_URL}/{session_id}/expire"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {Settings.PAYMONGO_TOKEN}",
        "accept": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return {"message": "Checkout session expired successfully", "response": response.json()}
    
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "error": str(http_err),
                "response": response.json()  # Or response.json() if you're confident it's valid JSON
            }
        )