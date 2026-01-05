from rapidfuzz import fuzz

# Palavras que indicam acessórios (penalizar)
ACCESSORY_KEYWORDS = [
    "capa", "case", "estojo",
    "suporte", "stand",
    "cabo", "hdmi", "usb",
    "adaptador", "carregador",
    "película", "protetor",
    "base", "dock",
    "tapete", "mouse pad",
    "headset", "fone",
    "controle", "joystick"
]

# Palavras que indicam produto principal (bónus)
CORE_PRODUCT_KEYWORDS = [
    "ps5", "playstation 5",
    "ps4", "playstation 4",
    "laptop", "notebook",
    "smartphone", "telemóvel",
    "monitor", "tv", "televisão",
    "pc", "computador"
]


def calculate_score(title: str, query: str, price: float | None) -> float:
    title_lower = title.lower()
    query_lower = query.lower()

    # Base: similaridade semântica
    score = fuzz.partial_ratio(title_lower, query_lower) * 2

    # Preço (não domina tudo)
    if price:
        score += max(0, 500 - price)

    # Penalizar acessórios
    for word in ACCESSORY_KEYWORDS:
        if word in title_lower and word not in query_lower:
            score -= 300

    # Bónus para produto principal
    for word in CORE_PRODUCT_KEYWORDS:
        if word in title_lower and word in query_lower:
            score += 400

    return score