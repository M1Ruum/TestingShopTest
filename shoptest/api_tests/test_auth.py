import pytest
from utils.api_client import APIClient
from utils.schema_validator import SchemaValidator
from config.settings import Config
import json
import os


class TestAuthAPI:
    """Tests for authentication API endpoints."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client instance."""
        return APIClient(Config.API_BASE_URL)
    
    @pytest.fixture
    def user_schema(self):
        """Load user schema."""
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'user_schema.json')
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def test_register_user_success(self, api_client, user_schema):
        """Test successful user registration."""
        payload = {
            "email": f"test_{pytest.test_id}@example.com",
            "username": f"testuser_{pytest.test_id}",
            "password": "TestPassword123!"
        }
        
        response = api_client.post('/auth/register', json=payload)
        
        # Validate status code
        SchemaValidator.validate_status_code(response.status_code, 201)
        
        # Validate response schema
        SchemaValidator.validate_schema(response.json(), user_schema)
        
        # Validate email format in response
        assert response.json()['email'] == payload['email']
    
    def test_register_user_duplicate_email(self, api_client):
        """Test registration with duplicate email - negative scenario."""
        payload = {
            "email": "existing@example.com",
            "username": "testuser",
            "password": "TestPassword123!"
        }
        
        # First registration
        api_client.post('/auth/register', json=payload)
        
        # Second registration with same email
        response = api_client.post('/auth/register', json=payload)
        
        # Should return 400 or 409
        assert response.status_code in [400, 409]
    
    def test_register_user_weak_password(self, api_client):
        """Test registration with weak password - boundary value testing."""
        payload = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "123"  # Too short
        }
        
        response = api_client.post('/auth/register', json=payload)
        
        # Should return 400 Bad Request
        assert response.status_code == 400
    
    def test_login_success(self, api_client):
        """Test successful login."""
        payload = {
            "email": Config.TEST_EMAIL,
            "password": Config.TEST_PASSWORD
        }
        
        response = api_client.post('/auth/login', json=payload)
        
        # Validate status code
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        # Validate token exists
        data = response.json()
        assert 'token' in data or 'access_token' in data
        
        # Set token for subsequent requests
        token = data.get('token') or data.get('access_token')
        api_client.set_token(token)
    
    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials - negative scenario."""
        payload = {
            "email": "invalid@example.com",
            "password": "WrongPassword123!"
        }
        
        response = api_client.post('/auth/login', json=payload)
        
        # Should return 401 Unauthorized
        assert response.status_code == 401
    
    def test_login_empty_email(self, api_client):
        """Test login with empty email - boundary value testing."""
        payload = {
            "email": "",
            "password": "TestPassword123!"
        }
        
        response = api_client.post('/auth/login', json=payload)
        
        # Should return 400 Bad Request
        assert response.status_code == 400
    
    def test_authenticated_request_without_token(self, api_client):
        """Test accessing protected endpoint without token - negative scenario."""
        response = api_client.get('/users/profile')
        
        # Should return 401 Unauthorized
        assert response.status_code == 401
