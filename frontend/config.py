import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

API_TIMEOUT_SECONDS = float(os.getenv("API_TIMEOUT_SECONDS", "15"))

MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
