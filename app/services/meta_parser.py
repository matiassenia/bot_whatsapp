from typing import Optional
from app.schemas.webhook import InboundMessage

def parse_inbound_message(payload: dict) -> Optional[InboundMessage]:
    """Parse the inbound message from the payload"""
    try:
        change = payload["entry"][0]["changes"][0]["value"]
        message = change["messages"][0]
        
        phone = message["from"]
        message_id = message["id"]
        timestamp = message.get("timestamp")
        
        text = None
        if "text" in message:
            text = message["text"]["body"]
            
        profile_name = contact["profile"]["name"]
        
        return InboundMessage(
            phone=phone,
            message_id=message_id,
            text=text,
            timestamp=timestamp,
            profile_name=profile_name
        )
    except (KeyError, IndexError, TypeError):
        return None

  