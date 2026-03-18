from enum import Enum


class ConversationState(str, Enum):
    NEW = "new"
    WELCOME = "welcome"

    BROWSING_MENU = "browsing_menu"
    BROWSING_PIZZAS = "browsing_pizzas"
    BROWSING_BEVERAGES = "browsing_beverages"
    BROWSING_DESSERTS = "browsing_desserts"

    CHOOSING_CATEGORY = "choosing_category"

    CHOOSING_PIZZA_TYPE = "choosing_pizza_type"
    CHOOSING_PIZZA_FLAVOR = "choosing_pizza_flavor"
    CHOOSING_HALF_AND_HALF = "choosing_half_and_half"

    CHOOSING_BEVERAGE = "choosing_beverage"
    CHOOSING_DESSERT = "choosing_dessert"

    CHOOSING_QUANTITY = "choosing_quantity"

    COLLECTING_MORE_ITEMS = "collecting_more_items"

    AWAITING_ADDRESS = "awaiting_address"
    AWAITING_CONFIRMATION = "awaiting_confirmation"

    HANDOFF_TO_HUMAN = "handoff_to_human"