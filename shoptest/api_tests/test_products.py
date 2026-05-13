import pytest
from utils.api_client import APIClient
from utils.schema_validator import SchemaValidator
from config.settings import Config
import json
import os


class TestProductsAPI:
    """Tests for products API endpoints."""
    
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
    def product_schema(self):
        """Load product schema."""
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'product_schema.json')
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def test_get_products_list(self, api_client, product_schema):
        """Test getting list of products."""
        response = api_client.get('/products')
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        assert isinstance(data, list)
        
        # Validate first product schema if list is not empty
        if len(data) > 0:
            SchemaValidator.validate_schema(data[0], product_schema)
    
    def test_get_product_by_id(self, api_client, product_schema):
        """Test getting single product by ID."""
        response = api_client.get('/products/1')
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        SchemaValidator.validate_schema(data, product_schema)
        assert data['id'] == 1
    
    def test_get_nonexistent_product(self, api_client):
        """Test getting nonexistent product - negative scenario."""
        response = api_client.get('/products/999999')
        
        # Should return 404 Not Found
        assert response.status_code == 404
    
    def test_create_product_success(self, api_client, product_schema):
        """Test successful product creation."""
        payload = {
            "name": "Test Product",
            "description": "Test product description",
            "price": 99.99,
            "quantity": 10,
            "category": "Electronics"
        }
        
        response = api_client.post('/products', json=payload)
        
        SchemaValidator.validate_status_code(response.status_code, 201)
        
        data = response.json()
        SchemaValidator.validate_schema(data, product_schema)
        assert data['name'] == payload['name']
        assert data['price'] == payload['price']
    
    def test_create_product_invalid_price(self, api_client):
        """Test creating product with negative price - boundary value testing."""
        payload = {
            "name": "Invalid Product",
            "description": "Product with negative price",
            "price": -10,
            "quantity": 5,
            "category": "Electronics"
        }
        
        response = api_client.post('/products', json=payload)
        
        # Should return 400 Bad Request
        assert response.status_code == 400
    
    def test_create_product_missing_required_field(self, api_client):
        """Test creating product without required field - negative scenario."""
        payload = {
            "name": "Incomplete Product",
            "description": "Missing price field"
            # price is missing
        }
        
        response = api_client.post('/products', json=payload)
        
        # Should return 400 Bad Request
        assert response.status_code == 400
    
    def test_update_product_success(self, api_client, product_schema):
        """Test successful product update."""
        payload = {
            "name": "Updated Product",
            "price": 149.99,
            "quantity": 20
        }
        
        response = api_client.put('/products/1', json=payload)
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        assert data['name'] == payload['name']
        assert data['price'] == payload['price']
    
    def test_delete_product_success(self, api_client):
        """Test successful product deletion."""
        # First create a product to delete
        create_payload = {
            "name": "Product to Delete",
            "price": 10.00,
            "quantity": 1,
            "category": "Test"
        }
        create_response = api_client.post('/products', json=create_payload)
        product_id = create_response.json()['id']
        
        # Delete the product
        response = api_client.delete(f'/products/{product_id}')
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        # Verify product is deleted
        get_response = api_client.get(f'/products/{product_id}')
        assert get_response.status_code == 404
    
    def test_filter_products_by_category(self, api_client):
        """Test filtering products by category."""
        response = api_client.get('/products', params={'category': 'Electronics'})
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        # All products should match the category filter
        for product in data:
            assert product['category'] == 'Electronics'
    
    def test_sort_products_by_price(self, api_client):
        """Test sorting products by price."""
        response = api_client.get('/products', params={'sort': 'price', 'order': 'asc'})
        
        SchemaValidator.validate_status_code(response.status_code, 200)
        
        data = response.json()
        # Verify prices are sorted ascending
        prices = [p['price'] for p in data]
        assert prices == sorted(prices)
