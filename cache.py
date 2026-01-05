import json
import time
import os
from config import CACHE_EXPIRATION

# Caminho absoluto da pasta do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta cache dentro do projeto
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# Garante que a pasta cache existe
os.makedirs(CACHE_DIR, exist_ok=True)


def cache_filename(query: str) -> str:
    safe_query = (
        query.lower()
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
    )
    return os.path.join(CACHE_DIR, f"cache_{safe_query}.json")


def load_cache(query: str):
    filename = cache_filename(query)

    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as f:
        cache = json.load(f)

    if time.time() - cache["timestamp"] > CACHE_EXPIRATION:
        return None

    return cache["data"]


def save_cache(query: str, data: list):
    filename = cache_filename(query)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": time.time(),
                "data": data
            },
            f,
            ensure_ascii=False,
            indent=2
        )