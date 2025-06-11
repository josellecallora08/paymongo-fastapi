# PayMongo FastAPI Integration

A FastAPI-based implementation that demonstrates integration with the PayMongo API. This includes handling user registration and authentication, pricing plan management, and payment processing through multiple flows (Card Payments, GCash, GrabPay, etc.).

## 📦 Features

- REST API with FastAPI
- JWT Authentication
- User Registration/Login
- Pricing Plan Management
- PayMongo Integration:
  - Card Payments via **Payment Intents**
  - E-wallet Payments via **Sources**
  - Hosted Checkout via **Checkout Links**
- Webhook-ready

---

## ⚙️ Prerequisites

- Python 3.10+
- FastAPI
- PostgreSQL or SQLite
- PayMongo account and secret key
- Ngrok (for local webhook testing)

---

## 🧭 Payment Flows

### 1. 🔐 Card Payment – Payment Intent Flow

**Use case**: Card payments with 3DS redirect and confirmation.

#### Flow

`User → Create PaymentMethod → Create PaymentIntent → Attach PaymentMethod → Redirect to 3DS → Webhook → Done`

#### Steps

1. **Create a Payment Method**

```json
POST /v1/payment_methods
Authorization: Basic <base64_secret>
Content-Type: application/json
{
    "type": "card",
    "details": {
    "card_number": "4343434343434345",
    "exp_month": 12,
    "exp_year": 2029,
    "cvc": "123"
    },
    "billing": {
    "name": "John Doe",
    "email": "john@example.com"
    }
}
```

_Sample Response_

```json
{
  "data": {
    "id": "pm_X27xpbNtVoeCTx8tu88hwUkn",
    "type": "payment_method",
    "attributes": {
      "livemode": false,
      "type": "gcash",
      "billing": null,
      "created_at": 1749679534,
      "updated_at": 1749679534,
      "details": null,
      "metadata": null
    }
  }
}
```

2. **Create a Payment Intent**

```json
POST /v1/payment_intents
{
"amount": 10000,
"currency": "PHP",
"payment_method_allowed": ["card"],
"description": "Pro Plan",
"capture_type": "automatic"
}
```

_Sample Response_

```json
{
  "data": {
    "id": "pi_87dBufgGJMYfLHG3nexJx8TR",
    "type": "payment_intent",
    "attributes": {
      "amount": 2000,
      "capture_type": "automatic",
      "client_key": "pi_87dBufgGJMYfLHG3nexJx8TR_client_J6XcfcK4WDjJAfbq3FSm2Pfo",
      "currency": "PHP",
      "description": null,
      "livemode": false,
      "original_amount": 2000,
      "statement_descriptor": "Sojdev",
      "status": "awaiting_payment_method",
      "last_payment_error": null,
      "payment_method_allowed": [
        "billease",
        "grab_pay",
        "dob",
        "paymaya",
        "card",
        "qrph",
        "gcash"
      ],
      "payments": [],
      "next_action": null,
      "payment_method_options": {
        "card": {
          "request_three_d_secure": "any"
        }
      },
      "metadata": null,
      "setup_future_usage": null,
      "created_at": 1749679577,
      "updated_at": 1749679577
    }
  }
}
```

3. **Attach Payment Method**

   ```json
   POST /v1/payment_intents/{intent_id}/attach
   Authorization: Basic <base64_secret>
   Content-Type: application/json
   {
   "payment_method": "{payment_method_id}",
   "return_url": "https://your-site.com/payment-success"
   }

   ```

   **Sample Response**

```json
{
  "data": {
    "id": "pi_87dBufgGJMYfLHG3nexJx8TR",
    "type": "payment_intent",
    "attributes": {
      "amount": 2000,
      "capture_type": "automatic",
      "client_key": "pi_87dBufgGJMYfLHG3nexJx8TR_client_J6XcfcK4WDjJAfbq3FSm2Pfo",
      "currency": "PHP",
      "description": null,
      "livemode": false,
      "original_amount": 2000,
      "statement_descriptor": "Sojdev",
      "status": "awaiting_next_action",
      "last_payment_error": null,
      "payment_method_allowed": [
        "billease",
        "grab_pay",
        "dob",
        "paymaya",
        "card",
        "qrph",
        "gcash"
      ],
      "payments": [],
      "next_action": {
        "type": "redirect",
        "redirect": {
          "url": "https://secure-authentication.paymongo.com/sources?id=src_YcZ6vrcfPF73yrLHrVYUDxku",
          "return_url": "https://www.google.com?payment_intent_id=pi_87dBufgGJMYfLHG3nexJx8TR"
        }
      },
      "payment_method_options": {
        "card": {
          "request_three_d_secure": "any"
        }
      },
      "metadata": null,
      "setup_future_usage": null,
      "created_at": 1749679577,
      "updated_at": 1749679656
    }
  }
}
```

4. **Redirect the user to the <pre> `next_action.redirect.url` </pre>.**
5. Listen to Webhook <pre>`payment_intent.succeeded` </pre>
   → You finalize business logic (e.g. activating a subscription)

### 2. E-wallet Payment – Source Flow (GCash, GrabPay)

#### Flow

`User → Create Source → Redirect to PayMongo → Webhook → Confirm Payment`

#### Steps

1. **Create a Source**

   ```json
   POST /v1/sources
   Authorization: Basic <base64_secret>
   Content-Type: application/json
   {
   "type": "gcash", // or "grab_pay"
   "amount": 10000,
   "currency": "PHP",
   "redirect": {
       "success": "http://localhost:3000/success",
       "failed": "http://localhost:3000/failed"
   },
   "billing": {
       "name": "Jane Doe",
       "email": "jane@example.com"
   }
   }
   ```

   **Sample Response**

```json
{
  "data": {
    "id": "src_gE5hRoEjkL14wt9GGwF2KFsE",
    "type": "source",
    "attributes": {
      "amount": 10000,
      "billing": null,
      "currency": "PHP",
      "description": null,
      "livemode": false,
      "redirect": {
        "checkout_url": "https://secure-authentication.paymongo.com/sources?id=src_gE5hRoEjkL14wt9GGwF2KFsE",
        "failed": "https://www.facebook.com",
        "success": "https://www.google.com"
      },
      "statement_descriptor": null,
      "status": "pending",
      "type": "gcash",
      "metadata": null,
      "created_at": 1749679093,
      "updated_at": 1749679093
    }
  }
}
```

2. **Redirect user to `source.redirect.checkout_url`**
3. **Listen for webhook `source.chargeable`**
   → Once the source becomes chargeable, create a payment:
4. **Create a Payment**

   ```json
   POST /v1/payments
   Authorization: Basic <base64_secret>
   Content-Type: application/json
   {
   "amount": 10000,
   "currency": "PHP",
   "source": {
   "id": "src_xxx",
   "type": "source"
   },
   "description": "Payment for Plan A"
   }
   ```

   **Sample Response**

```json
{
  "data": {
    "id": "pay_7WmZrAjmZqCAQYkHNLkrmYvS",
    "type": "payment",
    "attributes": {
      "access_url": null,
      "amount": 10000,
      "balance_transaction_id": "bal_txn_iWC2Jfv9GqdyJjaUZMZSgwuM",
      "billing": null,
      "currency": "PHP",
      "description": null,
      "disputed": false,
      "external_reference_number": null,
      "fee": 250,
      "instant_settlement": null,
      "livemode": false,
      "net_amount": 9750,
      "origin": "api",
      "payment_intent_id": null,
      "payout": null,
      "source": {
        "id": "src_gE5hRoEjkL14wt9GGwF2KFsE",
        "type": "gcash",
        "provider": {
          "id": null
        },
        "provider_id": null
      },
      "statement_descriptor": "Sojdev",
      "status": "paid",
      "tax_amount": null,
      "metadata": null,
      "promotion": null,
      "refunds": [],
      "taxes": [],
      "available_at": 1750150800,
      "created_at": 1749679224,
      "credited_at": 1750237200,
      "paid_at": 1749679224,
      "updated_at": 1749679224
    }
  }
}
```

### 3. 🧾 Checkout Link – Hosted Checkout Flow

#### Flow

`Create Checkout Link → Send to Customer → Redirect → Webhook → Confirmation`

#### Steps

1. **Create a Checkout Link**

```json
POST /v1/checkout_sessions
Authorization: Basic <base64_secret>
Content-Type: application/json
{
  "data": {
    "attributes": {
      "send_email_receipt": false,
      "show_description": true,
      "show_line_items": true,
      "line_items": [
        {
          "currency": "PHP",
          "amount": 2000,
          "name": "Credits",
          "quantity": 1,
          "description": "Sample"
        }
      ],
      "payment_method_types": [
        "gcash",
        "paymaya",
        "grab_pay",
        "card"
      ],
      "description": "Test Checkout"
    }
  }
}
```

**Sample Response**

```json
{
  "data": {
    "id": "cs_KYmJCN9G4GGUavErtq9Y4ZUz",
    "type": "checkout_session",
    "attributes": {
      "billing": {
        "address": {
          "city": null,
          "country": null,
          "line1": null,
          "line2": null,
          "postal_code": null,
          "state": null
        },
        "email": null,
        "name": null,
        "phone": null
      },
      "billing_information_fields_editable": "enabled",
      "cancel_url": null,
      "checkout_url": "https://checkout.paymongo.com/cs_KYmJCN9G4GGUavErtq9Y4ZUz_client_FaS4kiGSTuHQFJEJaMua7kc8#cGtfdGVzdF91Y0pLdEJyRllDTEZQUldmNXAzeWFqRVQ=",
      "client_key": "cs_KYmJCN9G4GGUavErtq9Y4ZUz_client_FaS4kiGSTuHQFJEJaMua7kc8",
      "customer_email": null,
      "description": "Test Checkout",
      "line_items": [
        {
          "amount": 2000,
          "currency": "PHP",
          "description": "Sample",
          "images": [],
          "name": "Credits",
          "quantity": 1
        }
      ],
      "livemode": false,
      "merchant": "Sojdev",
      "payments": [],
      "payment_intent": {
        "id": "pi_uzTQhLss1iumeizKNAT1e7a9",
        "type": "payment_intent",
        "attributes": {
          "amount": 2000,
          "capture_type": "automatic",
          "client_key": "pi_uzTQhLss1iumeizKNAT1e7a9_client_gNjHUzsoudRqYNCxXMoavczQ",
          "currency": "PHP",
          "description": "Test Checkout",
          "livemode": false,
          "original_amount": 2000,
          "statement_descriptor": "Sojdev",
          "status": "awaiting_payment_method",
          "last_payment_error": null,
          "payment_method_allowed": ["card", "paymaya", "grab_pay", "gcash"],
          "payments": [],
          "next_action": null,
          "payment_method_options": {
            "card": {
              "request_three_d_secure": "any"
            }
          },
          "metadata": null,
          "setup_future_usage": null,
          "created_at": 1749681480,
          "updated_at": 1749681480
        }
      },
      "payment_method_types": ["grab_pay", "card", "paymaya", "gcash"],
      "reference_number": null,
      "send_email_receipt": false,
      "show_description": true,
      "show_line_items": true,
      "status": "active",
      "success_url": null,
      "created_at": 1749681480,
      "updated_at": 1749681480,
      "metadata": null
    }
  }
}
```

2. **Redirect to `checkout_session.checkout_url`**
3. **Webhook triggers `checkout_session.paid` or `payment.paid`**
   → Activate plan or order fulfillment

## 🚦 Webhooks

Setup a webhook URL (e.g., via Ngrok)
Example webhook handler:

```
@app.post("/webhook")
async def webhook_listener(request: Request):
    payload = await request.body()
    signature = request.headers.get("paymongo-signature")

    if not verify_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = json.loads(payload)

    if event["data"]["type"] == "payment.paid":
        handle_payment_success(event)
```

**Sample Response**

```json
{
  "data": {
    "id": "evt_P2n7VqPF3qadtSKsspquWefL",
    "type": "event",
    "attributes": {
      "type": "payment.paid",
      "livemode": false,
      "data": {
        "id": "pay_VvXXYHW1tSco6pzG3y4jJX44",
        "type": "payment",
        "attributes": {
          "access_url": null,
          "amount": 2000,
          "balance_transaction_id": "bal_txn_AUxoJkxMAZRtnQ4PHRN9kduN",
          "billing": null,
          "currency": "PHP",
          "description": null,
          "disputed": false,
          "external_reference_number": null,
          "fee": 50,
          "instant_settlement": null,
          "livemode": false,
          "net_amount": 1950,
          "origin": "api",
          "payment_intent_id": "pi_87dBufgGJMYfLHG3nexJx8TR",
          "payout": null,
          "source": {
            "id": "src_YcZ6vrcfPF73yrLHrVYUDxku",
            "type": "gcash",
            "provider": {
              "id": null
            },
            "provider_id": null
          },
          "statement_descriptor": "Sojdev",
          "status": "paid",
          "tax_amount": null,
          "metadata": null,
          "promotion": null,
          "refunds": [],
          "taxes": [],
          "available_at": 1750150800,
          "created_at": 1749679676,
          "credited_at": 1750237200,
          "paid_at": 1749679676,
          "updated_at": 1749679676
        }
      },
      "previous_data": {},
      "pending_webhooks": 1,
      "created_at": 1749679676,
      "updated_at": 1749679676
    }
  }
}
```

## 🧪 Testing Locally

1. **Run your server:**
   `uvicorn app.main:app --reload`
2. **Expose your local server:**
   `ngrok http 8000`
3. Register the Ngrok URL as your webhook endpoint in PayMongo dashboard

## 🛠 Environment Example

`.env`

```
DATABASE_URL=postgresql://user:pass@localhost:5432/paymongo-db
PAYMONGO_SECRET_KEY=sk_test_xxxxx
FRONTEND_URL=http://localhost:3000
```

## 📁 Project Structure

```
app/
├── api/
│   └── v1/
│       └── auth.py
│       └── payment.py
├── core/
│   └── config.py
│   └── security.py
├── db/
│   └── init_db.py
│   └── session.py
├── models/
│   └── user.py
│   └── pricing_plan.py
├── schemas/
│   └── user.py
│   └── pricing_plan.py
└── main.py
```
