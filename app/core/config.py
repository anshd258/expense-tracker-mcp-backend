import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Database
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "expense_tracker")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # External APIs
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Application
    APP_NAME = "Expense Tracker API"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()