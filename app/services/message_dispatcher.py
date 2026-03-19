from app.schemas.webhook import InboundMessage
from app.services.conversation_service import handle_incoming_message
from app.services.whatsapp_client import send_text_message


def dispatch_incoming_message(message: InboundMessage) -> None:
    response_text = handle_incoming_message(message)
    
    print("INCOMING MESSAGE:", repr(message.text))
    print("BOT RESPONSE:", repr(response_text))


    if not response_text:
        return
#
#   send_text_message(
#       to=message.phone,
#       body=response_text,
#   )