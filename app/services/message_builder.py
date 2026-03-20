from app.data.menu import format_beverages, format_currency, format_desserts, format_pizzas


def build_welcome_message() -> str:
    return (
        "🍕 *Bienvenido/a a Aserrín Pizas*\n\n"
        "Podés elegir una de estas opciones:\n"
        "1️⃣ Ver menú completo\n"
        "2️⃣ Ver pizzas\n"
        "3️⃣ Ver bebidas\n"
        "4️⃣ Ver postres\n"
        "5️⃣ Hacer pedido\n"
        "6️⃣ Hablar con una persona \n\n"
        "También podés escribir directamente \n"
        "*pizza*, *bebida*, *postre*, *pedido*, o *humano*"
    )


def build_full_menu_message() -> str:
    return (
        "📋 *Menú Aserrín*\n\n"
        f"{format_pizzas()}\n\n"
        f"{format_beverages()}\n\n"
        f"{format_desserts()}\n\n"
        "Para empezar un pedido escribí *pedido* o *5*."
    )


def build_pizzas_message() -> str:
    return format_pizzas()


def build_beverages_message() -> str:
    return format_beverages()


def build_desserts_message() -> str:
    return format_desserts()


def build_choose_category_message() -> str:
    return (
        "🛒 ¿Qué querés agregar?\n\n"
        "Escribí:\n"
        "- *pizza*\n"
        "- *bebida*\n"
        "- *postre*\n"
        "- o *finalizar*"
    )


def build_choose_pizza_type_message() -> str:
    return (
        "🍕 ¿Qué tipo de pizza querés?\n\n"
        "Escribí:\n"
        "- *entera*\n"
        "- *mitad y mitad*"
    )


def build_choose_pizza_flavor_message() -> str:
    return (
        f"{format_pizzas()}\n\n"
        "Elegí un gusto por número o por nombre.\n"
        "Ejemplo: *1* o *muzza*"
    )


def build_choose_half_and_half_message() -> str:
    return (
        f"{format_pizzas()}\n\n"
        "👌 Pizza mitad y mitad.\n"
        "Mandame dos gustos por nombre.\n\n"
        "Ejemplo:\n"
        "*muzza y pepperoni*"
    )


def build_choose_beverage_message() -> str:
    return (
        f"{format_beverages()}\n\n"
        "Elegí una bebida por número o por nombre.\n"
        "Ejemplo: *2* o *coca 1.5*"
    )


def build_choose_dessert_message() -> str:
    return (
        f"{format_desserts()}\n\n"
        "Elegí un postre por número o por nombre.\n"
        "Ejemplo: *1* o *flan*"
    )


def build_ask_quantity_message(item_description: str) -> str:
    return (
        f"🧮 Elegiste: *{item_description}*\n\n"
        "¿Qué cantidad querés?\n"
        "Escribí un número. Ejemplo: *2*"
    )


def build_item_added_message(item_description: str, quantity: int) -> str:
    return (
        f"✅ Agregué: *{quantity} x {item_description}*\n\n"
        "¿Querés agregar algo más?\n"
        "- escribí *pizza*\n"
        "- escribí *bebida*\n"
        "- escribí *postre*\n"
        "- o escribí *finalizar*"
    )


def build_ask_address_message() -> str:
    return "📍 Pasame tu dirección para el pedido."


def build_order_summary_message(cart_items: list[dict], address: str) -> str:
    if not cart_items:
        items_text = "- Sin items"
        total = 0
    else:
        lines = []
        total = 0
        for item in cart_items:
            subtotal = item["quantity"] * item["unit_price"]
            total += subtotal
            lines.append(
                f"- {item['quantity']} x {item['description']} "
                f"({format_currency(item['unit_price'])} c/u) = {format_currency(subtotal)}"
            )
        items_text = "\n".join(lines)

    return (
        "🧾 *Resumen del pedido*\n\n"
        f"{items_text}\n\n"
        f"💵 *Total:* {format_currency(total)}\n"
        f"📍 *Dirección:* {address}\n\n"
        "Escribí *confirmar* para cerrar el pedido o *cancelar* para empezar de nuevo."
    )


def build_order_confirmed_message() -> str:
    return (
        "🎉 *Pedido confirmado*\n\n"
        "En breve seguimos con vos por acá para validar todo."
    )


def build_human_message() -> str:
    return "🙋 Te derivamos con una persona del equipo de Aserrín."


def build_fallback_message() -> str:
    return (
        "No entendí tu mensaje 😅\n\n"
        "Podés escribir:\n"
        "- *hola*\n"
        "- *menú*\n"
        "- *pizza*\n"
        "- *bebida*\n"
        "- *postre*\n"
        "- *pedido*\n"
        "- *humano*"
    )