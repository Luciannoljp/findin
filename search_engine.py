from serpapi_client import google_shopping_search
from normalizer import normalize_price, normalize_product
from ranker import calculate_score
from cache import load_cache, save_cache


def run_search(
    query: str,
    min_price: float | None = None,
    max_price: float | None = None,
    store: str | None = None,
    category: str | None = None,
    page: int = 1,
    page_size: int = 9
) -> dict:

    if not query or not query.strip():
        return {"results": [], "total": 0}

    cached = load_cache(query)
    if cached:
        processed = cached
    else:
        raw_results = google_shopping_search(query)
        processed = []

        for item in raw_results:
            title = item.get("title")
            if not title:
                continue

            price = normalize_price(item.get("price"))
            cat = normalize_product(title)

            score = calculate_score(title, query, price)
            if cat != "GENERIC_ELECTRONIC":
                score += 200

            processed.append({
                "title": title,
                "price": price,
                "store": item.get("source"),
                "location": item.get("delivery"),
                "link": item.get("link"),
                "category": cat,
                "score": score
            })

        processed.sort(key=lambda x: x["score"], reverse=True)
        save_cache(query, processed)

    # 🔎 FILTROS
    filtered = []
    for item in processed:
        if min_price is not None and (item["price"] is None or item["price"] < min_price):
            continue
        if max_price is not None and (item["price"] is None or item["price"] > max_price):
            continue
        if store and item["store"] and store.lower() not in item["store"].lower():
            continue
        if category and item["category"] != category:
            continue

        filtered.append(item)

    # 📄 PAGINAÇÃO REAL
    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "results": filtered[start:end],
        "total": total
    }