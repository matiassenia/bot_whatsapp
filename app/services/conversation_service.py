from app.schemas.webhook import InboundMessage
from app.services.message_builder import (
    build_fallback_message,
    build_human_message,
    build_menu_message,
    build_order_message,
    build_promos_message,
    build_welcome_message,
)


WELCOME_WORDS = {"hola", "buenas", "holaaa", "hello", "hi"}
MENU_WORDS = {"1", "menu", "menú"}
PROMO_WORDS = {"2", "promo", "promos"}
ORDER_WORDS = {"3", "pedido", "pedir"}
HUMAN_WORDS = {"4", "humano", "persona", "asesor"}


def handle_incoming_message(message: InboundMessage) -> str | None:
    if not message.text:
        return None

    text = message.text.strip().lower()

    if text in WELCOME_WORDS:
        return build_welcome_message()

    if text in MENU_WORDS:
        return build_menu_message()

    if text in PROMO_WORDS:
        return build_promos_message()

    if text in ORDER_WORDS:
        return build_order_message()

    if text in HUMAN_WORDS:
        return build_human_message()

    return build_fallback_message()