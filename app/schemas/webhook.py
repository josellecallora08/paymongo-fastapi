from pydantic import BaseModel
from typing import Optional, List  # Needed for Python <3.9

class WebhookEvent(BaseModel):
    url: str
    events: Optional[List[str]] = []  # Use list[str] if you're on Python 3.9+

class WebhookCreate(WebhookEvent):
    url: str
    events: Optional[List[str]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://example.com/webhook",
                "events": ["payment.created", "payment.failed"]
            }
        }
    }