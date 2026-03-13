# Aserrín WhatsApp Bot

Backend service that integrates the **WhatsApp Cloud API (Meta)** with a **FastAPI webhook** to receive and process incoming WhatsApp messages.

This project is the foundation of an automated ordering system for **Aserrín Pizzas**, allowing customers to interact with a bot through WhatsApp.

The system currently implements:

- WhatsApp Cloud API integration
- Webhook verification with Meta
- Reception of incoming messages
- Structured backend architecture ready for extensions
- Local development with FastAPI
- Public webhook exposure using ngrok

Future iterations will include:

- conversation state management
- order processing
- Redis for conversation state
- PostgreSQL for persistence
- menu system
- automated ordering flow

---

# Architecture

High level flow:
Customer (WhatsApp)
↓
WhatsApp Cloud API (Meta)
↓
Webhook HTTP request
↓
FastAPI backend
↓
Message processing



Webhook events are sent by Meta every time a user sends a message to the WhatsApp number.

---

# Project Structure

aserrin-whatsapp-bot/
│
├── app/
│ ├── main.py # FastAPI application entrypoint
│ │
│ ├── core/
│ │ └── config.py # Environment configuration
│ │
│ ├── api/
│ │ └── routes/
│ │ └── webhook.py # WhatsApp webhook endpoints
│ │
│ ├── services/
│ │ ├── meta_parser.py # Parses Meta webhook payloads (future step)
│ │ └── whatsapp_client.py # Sends messages through WhatsApp API (future step)
│ │
│ └── schemas/
│ └── webhook.py # Data schemas for webhook payloads
│
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md


---

# Requirements

- Python 3.10+
- Meta Developer account
- WhatsApp Cloud API enabled
- ngrok

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


Values required from the **Meta Developer Console**.

---

# Running the Application

Start the FastAPI server:


uvicorn app.main:app --reload --port 8000


Test health endpoint:


http://127.0.0.1:8000/health


Expected response:


{
"status": "ok"
}


---

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

- Meta webhook payload parser
- automatic responses
- conversation state machine
- order management
- Redis conversation state
- PostgreSQL persistence
- async workers
- analytics and monitoring

---

# Tech Stack

- FastAPI
- WhatsApp Cloud API
- Python
- ngrok