import os
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Fallback for development only - should be set in production
    SECRET_KEY = "dev-secret-key-change-in-production"
    import warnings
    warnings.warn("SECRET_KEY not set in environment. Using default dev key. This is insecure for production!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Token expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

