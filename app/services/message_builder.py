from app.data.menu import MENU_TEXT, PROMOS_TEXT, ORDER_TEXT, HUMAN_TEXT


def build_welcome_message() -> str:
    return (
        "🍕 *Bienvenido a Aserrín*\n\n"
        "Elegí una opción:\n"
        "1️⃣ Ver menú\n"
        "2️⃣ Ver promos\n"
        "3️⃣ Hacer pedido\n"
        "4️⃣ Hablar con humano"
    )


def build_menu_message() -> str:
    return MENU_TEXT


def build_promos_message() -> str:
    return PROMOS_TEXT


def build_order_message() -> str:
    return ORDER_TEXT


def build_human_message() -> str:
    return HUMAN_TEXT


def build_fallback_message() -> str:
    return (
        "No entendí tu mensaje 😅\n\n"
        "Podés escribir:\n"
        "1 para ver menú\n"
        "2 para ver promos\n"
        "3 para hacer pedido\n"
        "4 para hablar con humano"
    )