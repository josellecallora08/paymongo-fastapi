from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.db.session import get_db
import hmac, hashlib
import os

router = APIRouter()

@router.post("/payment-webhook")
async def handle_webhook(request: Request, db=Depends(get_db)):
    body = await request.body()
    print(f"Received webhook body: {body.decode('utf-8')}")
    return (
        {"message": "Webhook received successfully", "status": "success"}
        if hmac.compare_digest(
            request.headers.get("X-PayMongo-Signature", ""),
            hmac.new(
                os.environ.get("PAYMONGO_SECRET_KEY", "").encode(),
                body,
                hashlib.sha256
            ).hexdigest()
        )
        else HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")
    )
