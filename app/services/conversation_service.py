import re
import unicodedata

from app.data.menu import (
    BEVERAGE_INDEX_MAP,
    BEVERAGE_KEYWORDS,
    BEVERAGES,
    DESSERT_INDEX_MAP,
    DESSERT_KEYWORDS,
    DESSERTS,
    PIZZA_INDEX_MAP,
    PIZZA_KEYWORDS,
    PIZZAS,
)
from app.schemas.conversation_state import ConversationState
from app.schemas.webhook import InboundMessage
from app.services.conversation_store import get_conversation, reset_conversation, save_conversation
from app.services.message_builder import (
    build_ask_address_message,
    build_ask_quantity_message,
    build_beverages_message,
    build_choose_beverage_message,
    build_choose_category_message,
    build_choose_dessert_message,
    build_choose_half_and_half_message,
    build_choose_pizza_flavor_message,
    build_choose_pizza_type_message,
    build_desserts_message,
    build_fallback_message,
    build_full_menu_message,
    build_human_message,
    build_item_added_message,
    build_order_confirmed_message,
    build_order_summary_message,
    build_pizzas_message,
    build_welcome_message,
)

WELCOME_WORDS = {"hola", "holaaa", "buenas", "buenass", "hello", "hi"}
MENU_WORDS = {"1", "menu", "menú"}
PIZZA_MENU_WORDS = {"2", "pizza", "pizzas"}
BEVERAGE_MENU_WORDS = {"3", "bebida", "bebidas"}
DESSERT_MENU_WORDS = {"4", "postre", "postres"}
ORDER_WORDS = {"5", "pedido", "pedir"}
HUMAN_WORDS = {"6", "humano", "persona", "asesor"}

HALF_WORDS = {"mitad y mitad", "mitad", "half"}
WHOLE_WORDS = {"entera", "completa", "pizza entera"}

FINALIZE_WORDS = {"finalizar", "terminar", "listo"}
CONFIRM_WORDS = {"confirmar", "si", "sí", "ok", "dale"}
CANCEL_WORDS = {"cancelar", "no"}

CATEGORY_PIZZA_WORDS = {"pizza", "pizzas"}
CATEGORY_BEVERAGE_WORDS = {"bebida", "bebidas"}
CATEGORY_DESSERT_WORDS = {"postre", "postres"}


def _normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text


def _extract_quantity(text: str) -> int | None:
    text = text.strip()
    if text.isdigit():
        value = int(text)
        if 1 <= value <= 50:
            return value
    return None


def _find_pizza_key(text: str) -> str | None:
    if text in PIZZA_INDEX_MAP:
        return PIZZA_INDEX_MAP[text]

    for keyword, key in PIZZA_KEYWORDS.items():
        normalized_keyword = _normalize_text(keyword)
        if normalized_keyword in text:
            return key
    return None


def _find_beverage_key(text: str) -> str | None:
    if text in BEVERAGE_INDEX_MAP:
        return BEVERAGE_INDEX_MAP[text]

    for keyword, key in BEVERAGE_KEYWORDS.items():
        normalized_keyword = _normalize_text(keyword)
        if normalized_keyword in text:
            return key
    return None


def _find_dessert_key(text: str) -> str | None:
    if text in DESSERT_INDEX_MAP:
        return DESSERT_INDEX_MAP[text]

    for keyword, key in DESSERT_KEYWORDS.items():
        normalized_keyword = _normalize_text(keyword)
        if normalized_keyword in text:
            return key
    return None


def _extract_half_and_half(text: str) -> tuple[str, str] | None:
    matches = []

    for keyword, key in PIZZA_KEYWORDS.items():
        normalized_keyword = _normalize_text(keyword)
        if normalized_keyword in text and key not in matches:
            matches.append(key)

    if len(matches) >= 2:
        return matches[0], matches[1]

    return None


def _build_whole_pizza_pending(pizza_key: str) -> dict:
    pizza = PIZZAS[pizza_key]
    return {
        "category": "pizza",
        "type": "whole",
        "key": pizza_key,
        "description": f"Pizza entera de {pizza['name']}",
        "unit_price": pizza["price"],
    }


def _build_half_pizza_pending(first_key: str, second_key: str) -> dict:
    first = PIZZAS[first_key]
    second = PIZZAS[second_key]
    unit_price = max(first["price"], second["price"])

    return {
        "category": "pizza",
        "type": "half_and_half",
        "key": f"{first_key}+{second_key}",
        "description": f"Pizza mitad {first['name']} y mitad {second['name']}",
        "unit_price": unit_price,
    }


def _build_beverage_pending(beverage_key: str) -> dict:
    bev = BEVERAGES[beverage_key]
    return {
        "category": "beverage",
        "type": "single",
        "key": beverage_key,
        "description": bev["name"],
        "unit_price": bev["price"],
    }


def _build_dessert_pending(dessert_key: str) -> dict:
    dessert = DESSERTS[dessert_key]
    return {
        "category": "dessert",
        "type": "single",
        "key": dessert_key,
        "description": dessert["name"],
        "unit_price": dessert["price"],
    }


def _append_pending_item_to_cart(conversation: dict, quantity: int) -> dict:
    pending_item = conversation["pending_item"]
    cart_item = {
        "category": pending_item["category"],
        "type": pending_item["type"],
        "key": pending_item["key"],
        "description": pending_item["description"],
        "quantity": quantity,
        "unit_price": pending_item["unit_price"],
    }
    conversation["cart"].append(cart_item)
    conversation["pending_item"] = None
    return cart_item


def handle_incoming_message(message: InboundMessage) -> str | None:
    if not message.text:
        return None

    raw_text = message.text.strip()
    text = _normalize_text(raw_text)

    conversation = get_conversation(message.phone)
    state = conversation["state"]
    conversation["last_message"] = raw_text

    if text in WELCOME_WORDS:
        conversation["state"] = ConversationState.WELCOME
        save_conversation(message.phone, conversation)
        return build_welcome_message()

    if text in MENU_WORDS:
        conversation["state"] = ConversationState.BROWSING_MENU
        save_conversation(message.phone, conversation)
        return build_full_menu_message()

    if text in PIZZA_MENU_WORDS and state not in {
        ConversationState.COLLECTING_MORE_ITEMS,
        ConversationState.CHOOSING_CATEGORY,
    }:
        conversation["state"] = ConversationState.BROWSING_PIZZAS
        save_conversation(message.phone, conversation)
        return build_pizzas_message()

    if text in BEVERAGE_MENU_WORDS and state not in {
        ConversationState.COLLECTING_MORE_ITEMS,
        ConversationState.CHOOSING_CATEGORY,
    }:
        conversation["state"] = ConversationState.BROWSING_BEVERAGES
        save_conversation(message.phone, conversation)
        return build_beverages_message()

    if text in DESSERT_MENU_WORDS and state not in {
        ConversationState.COLLECTING_MORE_ITEMS,
        ConversationState.CHOOSING_CATEGORY,
    }:
        conversation["state"] = ConversationState.BROWSING_DESSERTS
        save_conversation(message.phone, conversation)
        return build_desserts_message()

    if text in ORDER_WORDS:
        conversation["state"] = ConversationState.CHOOSING_CATEGORY
        save_conversation(message.phone, conversation)
        return build_choose_category_message()

    if text in HUMAN_WORDS:
        conversation["state"] = ConversationState.HANDOFF_TO_HUMAN
        save_conversation(message.phone, conversation)
        return build_human_message()

    if state in {ConversationState.CHOOSING_CATEGORY, ConversationState.COLLECTING_MORE_ITEMS}:
        if text in CATEGORY_PIZZA_WORDS:
            conversation["state"] = ConversationState.CHOOSING_PIZZA_TYPE
            save_conversation(message.phone, conversation)
            return build_choose_pizza_type_message()

        if text in CATEGORY_BEVERAGE_WORDS:
            conversation["state"] = ConversationState.CHOOSING_BEVERAGE
            save_conversation(message.phone, conversation)
            return build_choose_beverage_message()

        if text in CATEGORY_DESSERT_WORDS:
            conversation["state"] = ConversationState.CHOOSING_DESSERT
            save_conversation(message.phone, conversation)
            return build_choose_dessert_message()

        if text in FINALIZE_WORDS:
            if not conversation["cart"]:
                save_conversation(message.phone, conversation)
                return "Todavía no agregaste productos. Escribí *pizza*, *bebida* o *postre*."
            conversation["state"] = ConversationState.AWAITING_ADDRESS
            save_conversation(message.phone, conversation)
            return build_ask_address_message()

    if state == ConversationState.CHOOSING_PIZZA_TYPE:
        if text in WHOLE_WORDS:
            conversation["state"] = ConversationState.CHOOSING_PIZZA_FLAVOR
            save_conversation(message.phone, conversation)
            return build_choose_pizza_flavor_message()

        if text in HALF_WORDS:
            conversation["state"] = ConversationState.CHOOSING_HALF_AND_HALF
            save_conversation(message.phone, conversation)
            return build_choose_half_and_half_message()

    if state == ConversationState.CHOOSING_PIZZA_FLAVOR:
        pizza_key = _find_pizza_key(text)
        if pizza_key:
            pending_item = _build_whole_pizza_pending(pizza_key)
            conversation["pending_item"] = pending_item
            conversation["state"] = ConversationState.CHOOSING_QUANTITY
            save_conversation(message.phone, conversation)
            return build_ask_quantity_message(pending_item["description"])

    if state == ConversationState.CHOOSING_HALF_AND_HALF:
        half_combo = _extract_half_and_half(text)
        if half_combo:
            first_key, second_key = half_combo
            pending_item = _build_half_pizza_pending(first_key, second_key)
            conversation["pending_item"] = pending_item
            conversation["state"] = ConversationState.CHOOSING_QUANTITY
            save_conversation(message.phone, conversation)
            return build_ask_quantity_message(pending_item["description"])

    if state == ConversationState.CHOOSING_BEVERAGE:
        beverage_key = _find_beverage_key(text)
        if beverage_key:
            pending_item = _build_beverage_pending(beverage_key)
            conversation["pending_item"] = pending_item
            conversation["state"] = ConversationState.CHOOSING_QUANTITY
            save_conversation(message.phone, conversation)
            return build_ask_quantity_message(pending_item["description"])

    if state == ConversationState.CHOOSING_DESSERT:
        dessert_key = _find_dessert_key(text)
        if dessert_key:
            pending_item = _build_dessert_pending(dessert_key)
            conversation["pending_item"] = pending_item
            conversation["state"] = ConversationState.CHOOSING_QUANTITY
            save_conversation(message.phone, conversation)
            return build_ask_quantity_message(pending_item["description"])

    if state == ConversationState.CHOOSING_QUANTITY:
        quantity = _extract_quantity(text)
        if quantity and conversation["pending_item"]:
            cart_item = _append_pending_item_to_cart(conversation, quantity)
            conversation["state"] = ConversationState.COLLECTING_MORE_ITEMS
            save_conversation(message.phone, conversation)
            return build_item_added_message(
                item_description=cart_item["description"],
                quantity=cart_item["quantity"],
            )

    if state == ConversationState.AWAITING_ADDRESS:
        conversation["address"] = raw_text
        conversation["state"] = ConversationState.AWAITING_CONFIRMATION
        save_conversation(message.phone, conversation)
        return build_order_summary_message(
            cart_items=conversation["cart"],
            address=conversation["address"],
        )

    if state == ConversationState.AWAITING_CONFIRMATION:
        if text in CONFIRM_WORDS:
            reset_conversation(message.phone)
            return build_order_confirmed_message()

        if text in CANCEL_WORDS:
            reset_conversation(message.phone)
            return "Pedido cancelado. Escribí *hola* para empezar de nuevo."

    save_conversation(message.phone, conversation)
    return build_fallback_message()