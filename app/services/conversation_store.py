from copy import deepcopy

from app.schemas.conversation_state import ConversationState


DEFAULT_CONVERSATION = {
    "state": ConversationState.NEW,
    "cart": [],
    "address": None,
    "pending_item": None,
    "last_message": None,
}

conversation_store: dict[str, dict] = {}


def get_conversation(phone: str) -> dict:
    existing = conversation_store.get(phone)
    if existing:
        return existing

    new_conversation = deepcopy(DEFAULT_CONVERSATION)
    conversation_store[phone] = new_conversation
    return new_conversation


def save_conversation(phone: str, conversation: dict) -> None:
    conversation_store[phone] = conversation


def reset_conversation(phone: str) -> dict:
    conversation_store[phone] = deepcopy(DEFAULT_CONVERSATION)
    return conversation_store[phone]