def normalize_price(price_str):
    if not price_str:
        return None

    try:
        return float(
            price_str.replace("€", "")
                     .replace(".", "")
                     .replace(",", ".")
                     .strip()
        )
    except ValueError:
        return None


def normalize_product(title: str) -> str:
    title = title.lower()

    if "ps5" in title or "playstation 5" in title:
        return "PS5"
    if "ps4" in title or "playstation 4" in title:
        return "PS4"
    if "laptop" in title or "notebook" in title:
        return "LAPTOP"
    if "smartphone" in title or "telemóvel" in title:
        return "SMARTPHONE"
    if "pc" in title or "computador" in title:
        return "PC"

    # ⚠️ IMPORTANTE:
    # Não descartar outros eletrónicos
    return "GENERIC_ELECTRONIC"