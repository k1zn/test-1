DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21
SAVE10_DISCOUNT_RATE = 0.10
SAVE20_DISCOUNT_RATE = 0.20
SAVE20_FALLBACK_RATE = 0.05
SAVE20_THRESHOLD = 200
VIP_DISCOUNT_HIGH = 50
VIP_DISCOUNT_LOW = 10
VIP_THRESHOLD = 100


def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency


def validate_request(user_id, items, currency):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    
    normalized_currency = currency if currency is not None else DEFAULT_CURRENCY
    return normalized_currency


def validate_items(items):
    if type(items) is not list:
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0:
            raise ValueError("price must be positive")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")


def calculate_subtotal(items):
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["qty"]
    return subtotal


def calculate_discount(coupon, subtotal):
    if coupon is None or coupon == "":
        return 0
    elif coupon == "SAVE10":
        return int(subtotal * SAVE10_DISCOUNT_RATE)
    elif coupon == "SAVE20":
        if subtotal >= SAVE20_THRESHOLD:
            return int(subtotal * SAVE20_DISCOUNT_RATE)
        else:
            return int(subtotal * SAVE20_FALLBACK_RATE)
    elif coupon == "VIP":
        if subtotal < VIP_THRESHOLD:
            return VIP_DISCOUNT_LOW
        return VIP_DISCOUNT_HIGH
    else:
        raise ValueError("unknown coupon")


def calculate_tax(amount):
    return int(amount * TAX_RATE)


def generate_order_id(user_id, items_count):
    return f"{user_id}-{items_count}-X"


def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)
    
    currency = validate_request(user_id, items, currency)
    validate_items(items)
    
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(coupon, subtotal)
    
    total_after_discount = max(0, subtotal - discount)
    tax = calculate_tax(total_after_discount)
    total = total_after_discount + tax
    
    order_id = generate_order_id(user_id, len(items))
    
    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }