from fastapi import APIRouter, HTTPException, Query, Request
from app.core.config import settings
from app.services.meta_parser import extract_message_info, parse_inbound_message
from fastapi.responses import PlainTextResponse
from app.services.whatsapp_client import send_text_message

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(default=None, alias="hub.mode"),
    hub_challenge: str = Query(default=None, alias="hub.challenge"),
    hub_verify_token: str = Query(default=None, alias="hub.verify_token")
):

    if hub_mode == "subscribe" and hub_verify_token == settings.verify_token:
        return PlainTextResponse(content=hub_challenge)

    raise HTTPException(status_code=403, detail="Invalid verify token")


@router.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    
    message = parse_inbound_message(payload)

    print("-------------WEBHOOK RECEIVED-------------------")
    print(message)
    print("--------------------------------")

    if message and message.text:
        incoming_text = message.text.strip().lower()
        from_number = message.phone
        
        if incoming_text == "hola":
            send_text_message(
            to=from_number, 
           body="¡Hola! Bienvenido a Aserrín\n\n1️⃣ Ver menú\n2️⃣ Ver promos\n3️⃣ Hacer pedido"
            )

    return {"status": "received"}