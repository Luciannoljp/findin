from serpapi import GoogleSearch
from config import (
    SERPAPI_KEY,
    LANGUAGE,
    COUNTRY,
    SERPAPI_TIMEOUT,
    SERPAPI_MAX_RETRIES
)
import time
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def google_shopping_search(query: str) -> list:
    params = {
        "engine": "google_shopping",
        "q": query,
        "hl": LANGUAGE,
        "gl": COUNTRY,
        "api_key": SERPAPI_KEY
    }

    for attempt in range(1, SERPAPI_MAX_RETRIES + 1):
        try:
            search = GoogleSearch(params)
            search.timeout = SERPAPI_TIMEOUT

            results = search.get_dict()
            return results.get("shopping_results", [])

        except Exception as e:
            logging.error(
                f"SerpApi falhou (tentativa {attempt}/{SERPAPI_MAX_RETRIES}): {e}"
            )
            time.sleep(1)

    # Falha total controlada
    return []