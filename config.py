import os

try:
    # Só carrega .env se existir (ambiente local)
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Em produção (Render), dotenv não é necessário
    pass


# =========================
# API
# =========================
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    raise RuntimeError("SERPAPI_KEY não definida nas variáveis de ambiente")


# =========================
# Localização
# =========================
LANGUAGE = "pt"
COUNTRY = "pt"


# =========================
# Cache
# =========================
CACHE_EXPIRATION = 21600  # 6 horas


# =========================
# Robustez (NÍVEL 4)
# =========================
SERPAPI_TIMEOUT = 10      # segundos
SERPAPI_MAX_RETRIES = 3  # tentativas