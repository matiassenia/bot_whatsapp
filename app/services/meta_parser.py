from typing import Optional
from app.schemas.webhook import InboundMessage


def parse_inbound_message(payload: dict) -> Optional[InboundMessage]:

    try:
        change = payload["entry"][0]["changes"][0]["value"]

        # si no hay mensajes, ignorar
        if "messages" not in change:
            return None

        message = change["messages"][0]
        contact = change.get("contacts", [{}])[0]

        phone = message.get("from")
        message_id = message.get("id")
        timestamp = message.get("timestamp")

        text = None
        if "text" in message:
            text = message["text"]["body"]

        profile_name = contact.get("profile", {}).get("name")

        return InboundMessage(
            phone=phone,
            message_id=message_id,
            text=text,
            timestamp=timestamp,
            profile_name=profile_name,
        )

    except Exception:
        return None