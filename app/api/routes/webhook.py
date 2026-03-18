import json
import traceback

from fastapi import APIRouter, HTTPException, Query, Request
from app.core.config import settings

from app.services.message_dispatcher import dispatch_incoming_message

from app.services.meta_parser import  parse_inbound_message
from fastapi.responses import PlainTextResponse


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
    print("RAW PAYLOAD:", json.dumps(payload, indent=2, ensure_ascii=False))
    print("--------------------------------")
    
    message = parse_inbound_message(payload)
    
    if message:
        print("PHONE:", message.phone)
        print("MESSAGE ID:", message.message_id)
        print("TEXT:", message.text)
        print("TIMESTAMP:", message.timestamp)
    else:
        print("No actionable inbound message found")
        
    print("--------------------------------")

    if message: 
        try:
            dispatch_incoming_message(message)
        except Exception as e:
            print("Error dispatching message:")
            traceback.print_exc()
            print("--------------------------------")
            
    return {"status": "received"}