import os
from dotenv import load_dotenv

load_dotenv()

# API
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Localização
LANGUAGE = "pt"
COUNTRY = "pt"

# Cache
CACHE_EXPIRATION = 21600  # 6 horas

# Robustez (NÍVEL 4)
SERPAPI_TIMEOUT = 10      # segundos
SERPAPI_MAX_RETRIES = 3  # tentativas