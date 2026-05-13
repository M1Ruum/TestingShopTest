import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for test settings."""
    
    # API Settings
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api/v1')
    
    # UI Settings
    UI_BASE_URL = os.getenv('UI_BASE_URL', 'http://localhost:3000')
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', 10))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', 30))
    
    # Test Credentials
    TEST_EMAIL = os.getenv('TEST_EMAIL', 'test@example.com')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'TestPassword123!')
    
    # Database Settings
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'shop_test')
    DB_USER = os.getenv('DB_USER', 'test_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'test_password')
