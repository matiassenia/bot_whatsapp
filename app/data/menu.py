PIZZAS = {
    "muzza": {"name": "Muzzarella", "price": 10000},
    "pepperoni": {"name": "Pepperoni", "price": 13000},
    "fugazzeta": {"name": "Fugazzeta", "price": 12000},
    "tres_quesos": {"name": "Tres quesos", "price": 13500},
    "napolitana": {"name": "Napolitana", "price": 12000},
    "jamon_morron": {"name": "Jamón y morrón", "price": 13500},
}

BEVERAGES = {
    "coca_500": {"name": "Coca Cola 500ml", "price": 2500},
    "coca_15": {"name": "Coca Cola 1.5L", "price": 4500},
    "sprite_15": {"name": "Sprite 1.5L", "price": 4500},
    "agua": {"name": "Agua", "price": 1800},
}

DESSERTS = {
    "flan": {"name": "Flan", "price": 3500},
    "helado": {"name": "Helado", "price": 4000},
    "brownie": {"name": "Brownie", "price": 3200},
}


PIZZA_KEYWORDS = {
    "muzza": "muzza",
    "muzzarella": "muzza",
    "pepperoni": "pepperoni",
    "fugazzeta": "fugazzeta",
    "fuga": "fugazzeta",
    "tres quesos": "tres_quesos",
    "3 quesos": "tres_quesos",
    "napolitana": "napolitana",
    "jamon y morron": "jamon_morron",
    "jamón y morrón": "jamon_morron",
    "jamon morron": "jamon_morron",
    "jamón morrón": "jamon_morron",
}

BEVERAGE_KEYWORDS = {
    "coca 500": "coca_500",
    "coca cola 500": "coca_500",
    "coca 1.5": "coca_15",
    "coca cola 1.5": "coca_15",
    "sprite": "sprite_15",
    "agua": "agua",
}

DESSERT_KEYWORDS = {
    "flan": "flan",
    "helado": "helado",
    "brownie": "brownie",
}


PIZZA_INDEX_MAP = {
    "1": "muzza",
    "2": "pepperoni",
    "3": "fugazzeta",
    "4": "tres_quesos",
    "5": "napolitana",
    "6": "jamon_morron",
}

BEVERAGE_INDEX_MAP = {
    "1": "coca_500",
    "2": "coca_15",
    "3": "sprite_15",
    "4": "agua",
}

DESSERT_INDEX_MAP = {
    "1": "flan",
    "2": "helado",
    "3": "brownie",
}


def format_currency(value: int) -> str:
    return f"${value:,}".replace(",", ".")


def format_pizzas() -> str:
    lines = ["🍕 *Pizzas*"]
    for idx, key in enumerate(PIZZAS.keys(), start=1):
        pizza = PIZZAS[key]
        lines.append(f"{idx}. {pizza['name']} - {format_currency(pizza['price'])}")
    lines.append("")
    lines.append("Podés pedir pizza *entera* o escribir *mitad y mitad*.")
    return "\n".join(lines)


def format_beverages() -> str:
    lines = ["🥤 *Bebidas*"]
    for idx, key in enumerate(BEVERAGES.keys(), start=1):
        bev = BEVERAGES[key]
        lines.append(f"{idx}. {bev['name']} - {format_currency(bev['price'])}")
    return "\n".join(lines)


def format_desserts() -> str:
    lines = ["🍰 *Postres*"]
    for idx, key in enumerate(DESSERTS.keys(), start=1):
        dessert = DESSERTS[key]
        lines.append(f"{idx}. {dessert['name']} - {format_currency(dessert['price'])}")
    return "\n".join(lines)