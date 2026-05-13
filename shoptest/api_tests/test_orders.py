import pytest
from utils.api_client import APIClient
from utils.schema_validator import SchemaValidator
from config.settings import Config
import json
import os


class TestOrdersAPI:
    """Tests for orders API endpoints."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client instance with authentication."""
        client = APIClient(Config.API_BASE_URL)
        # Login and set token
        login_response = client.post('/auth/login', json={
            "email": Config.TEST_EMAIL,
            "password": Config.TEST_PASSWORD
        })
        if login_response.status_code == 200:
            data = login_response.json()
            token = data.get('token') or data.get('access_token')
            client.set_token(token)
        return client
    
    @pytest.fixture
    def order_schema(self):
        """Load order schema."""
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'order_schema.json')
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def test_get_orders_list(self, api_client, order_schema):
        """Test getting list of orders."""
        response = api_client.get('/orders')
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        assert isinstance(data, list)
        
        # Validate first order schema if list is not empty
        if len(data) > 0:
            SchemaValidator.validate_schema(data[0], order_schema)
    
    def test_get_order_by_id(self, api_client, order_schema):
        """Test getting single order by ID."""
        response = api_client.get('/orders/1')
        
        # May return 200 or 404 depending on existing data
        if response.status_code == 200:
            data = response.json()
            SchemaValidator.validate_schema(data, order_schema)
            assert data['id'] == 1
    
    def test_create_order_success(self, api_client, order_schema):
        """Test successful order creation."""
        payload = {
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2
                }
            ]
        }
        
        response = api_client.post('/orders', json=payload)
        
        SchemaValidator.validate_status_code(response.status_code, 201)
        
        data = response.json()
        SchemaValidator.validate_schema(data, order_schema)
        assert data['status'] == 'pending'
        assert len(data['items']) > 0
    
    def test_create_order_empty_items(self, api_client):
        """Test creating order with empty items - negative scenario."""
        payload = {
            "items": []
        }
        
        response = api_client.post('/orders', json=payload)
        
        # Should return 400 Bad Request
        assert response.status_code == 400
    
    def test_create_order_invalid_product(self, api_client):
        """Test creating order with nonexistent product - boundary value testing."""
        payload = {
            "items": [
                {
                    "product_id": 999999,
                    "quantity": 1
                }
            ]
        }
        
        response = api_client.post('/orders', json=payload)
        
        # Should return 400 or 404
        assert response.status_code in [400, 404]
    
    def test_create_order_zero_quantity(self, api_client):
        """Test creating order with zero quantity - boundary value testing."""
        payload = {
            "items": [
                {
                    "product_id": 1,
                    "quantity": 0
                }
            ]
        }
        
        response = api_client.post('/orders', json=payload)
        
        # Should return 400 Bad Request
        assert response.status_code == 400
    
    def test_update_order_status(self, api_client, order_schema):
        """Test updating order status."""
        # First create an order
        create_payload = {"items": [{"product_id": 1, "quantity": 1}]}
        create_response = api_client.post('/orders', json=create_payload)
        order_id = create_response.json()['id']
        
        # Update status
        update_payload = {"status": "confirmed"}
        response = api_client.patch(f'/orders/{order_id}', json=update_payload)
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        assert data['status'] == 'confirmed'
    
    def test_cancel_order(self, api_client):
        """Test cancelling an order."""
        # First create an order
        create_payload = {"items": [{"product_id": 1, "quantity": 1}]}
        create_response = api_client.post('/orders', json=create_payload)
        order_id = create_response.json()['id']
        
        # Cancel the order
        response = api_client.patch(f'/orders/{order_id}/cancel')
        
        # Should return 200 or 204
        assert response.status_code in [200, 204]
        
        # Verify order is cancelled
        get_response = api_client.get(f'/orders/{order_id}')
        if get_response.status_code == 200:
            assert get_response.json()['status'] == 'cancelled'
    
    def test_get_order_unauthorized(self):
        """Test getting order without authentication - negative scenario."""
        client = APIClient(Config.API_BASE_URL)
        response = client.get('/orders/1')
        
        # Should return 401 Unauthorized
        assert response.status_code == 401
    
    def test_order_total_calculation(self, api_client, order_schema):
        """Test that order total is calculated correctly."""
        payload = {
            "items": [
                {"product_id": 1, "quantity": 2},
                {"product_id": 2, "quantity": 1}
            ]
        }
        
        response = api_client.post('/orders', json=payload)
        
        if response.status_code == 201:
            data = response.json()
            SchemaValidator.validate_schema(data, order_schema)
            
            # Verify total_amount is positive
            assert data['total_amount'] > 0
