# Aserrín WhatsApp Bot

Backend service for **Aserrín Pizzas** built with **FastAPI** and integrated with the **WhatsApp Cloud API (Meta)**.

This project implements the foundation of a conversational ordering bot that can:

- receive inbound WhatsApp messages through a webhook
- verify the Meta webhook
- parse inbound Meta payloads into internal schemas
- manage a stateful conversation flow in memory
- show menus for pizzas, beverages, and desserts
- support pizza ordering, including **whole pizzas** and **half-and-half pizzas**
- collect quantities
- build a structured cart
- request delivery address
- generate an order summary with totals
- confirm or cancel orders
- simulate the full flow locally without relying on Meta delivery

---

# Current Features

- WhatsApp Cloud API integration
- Webhook verification with Meta
- FastAPI webhook endpoint for inbound messages
- Meta payload parser
- In-memory conversation state store
- Stateful order flow
- Menu browsing
- Product selection by text or number
- Half-and-half pizza support
- Quantity handling
- Cart summary generation
- Local simulator for order flow testing

---

# Architecture

High-level flow:

Customer (WhatsApp or local simulator)  
↓  
WhatsApp Cloud API (Meta) or local HTTP request  
↓  
FastAPI `/webhook` endpoint  
↓  
Meta payload parsing  
↓  
Message dispatcher  
↓  
Conversation service (state machine)  
↓  
Response generation  
↓  
Optional WhatsApp API delivery

---

# Conversation Flow

The bot currently supports a flow like this:

1. User says `hola`
2. Bot shows welcome message
3. User starts an order with `5` or `pedido`
4. User chooses a category: pizza, bebida, postre
5. User selects an item
6. Bot asks for quantity
7. User can continue adding items
8. User writes `finalizar`
9. Bot asks for address
10. Bot shows structured order summary
11. User confirms or cancels

Example supported order:

- 2 x half-and-half pizza (Muzzarella + Pepperoni)
- 1 x Coca Cola 1.5L
- delivery address
- final confirmation

---

# Project Structure

```text
aserrin-whatsapp-bot/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── api/
│   │   └── routes/
│   │       └── webhook.py
│   │
│   ├── data/
│   │   └── menu.py
│   │
│   ├── schemas/
│   │   ├── webhook.py
│   │   └── conversation_state.py
│   │
│   ├── services/
│   │   ├── meta_parser.py
│   │   ├── whatsapp_client.py
│   │   ├── message_dispatcher.py
│   │   ├── message_builder.py
│   │   ├── conversation_service.py
│   │   └── conversation_store.py
│
├── scripts/
│   └── test_order_flow.py
│
├── .env
├── requirements.txt
└── README.md

---

# Requirements

- Python 3.10+
- Meta Developer account
- WhatsApp Cloud API enabled
- ngrok (for public webhook testing)
- a valid access token if you want real outbound replies
---

# Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/aserrin-whatsapp-bot.git

cd aserrin-whatsapp-bot


Create virtual environment:


python -m venv venv


Activate it (Windows):


venv\Scripts\activate


Install dependencies:


pip install -r requirements.txt


---

# Environment Variables

Create a `.env` file in the root directory:


APP_NAME=Aserrin WhatsApp Bot
APP_ENV=development

VERIFY_TOKEN=aserrin_verify_token

WHATSAPP_ACCESS_TOKEN=YOUR_ACCESS_TOKEN
WHATSAPP_PHONE_NUMBER_ID=YOUR_PHONE_NUMBER_ID
WHATSAPP_API_VERSION=v22.0


These values required from the **Meta Developer Console**.

---

# Running the Application
-For local development without live reload issues:

Start the FastAPI server:


uvicorn app.main:app --reload --port 8000


Test health endpoint:


http://127.0.0.1:8000/health


Expected response:


{
"status": "ok"
}


#-Local Testing Wihout Meta

You can test the complete order flow locally without sending real sending real WhatsApp replies.

Impotant
If you Meta acces token is expired or you only want to test the internal conversation flow, temporarily comment out send_text_message(...) in:

app/services/message_dispatcher.py

# -Run the server

uvicorn app.main:app --port 8000

# Run the simulator

python scripts/test_order_flow.py

This will send a sequence of webhook requests that simulate a full customer order.

# Exposing the Webhook (ngrok)

Meta requires a **public URL** for webhook callbacks.

Run:

ngrok http 8000


You will get a public URL like:


https://abcd1234.ngrok-free.app


Webhook endpoint:


https://abcd1234.ngrok-free.app/webhook


---

# Configure Webhook in Meta

In **Meta Developer Console → WhatsApp → Configuration**

Set:

Callback URL


https://abcd1234.ngrok-free.app/webhook


Verify Token


aserrin_verify_token


Subscribe to field:


messages


---

# Testing the Integration

1. Send a message from your phone to the WhatsApp test number
2. Meta sends a webhook event
3. The backend receives the payload

You should see the webhook payload printed in the server logs.

---

# Next Steps

Planned improvements:

-Redis for convcersation state
-PostgreSql for order persistence
-real order entity and order items
-improved observability and sturctured logging
-better error handling
-production-ready WhatsApp reply delivery
-admin/operator handoff flow
-payment and delivery options

---

# Tech Stack

- Python
- FastAPI
- Pydantic
- Request
- WhatsApp Cloud API
- ngrok