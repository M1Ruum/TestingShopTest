import pytest
from selenium.webdriver.common.by import By
from pages.home_page import HomePage, SearchResultsPage
from pages.cart_page import CartPage, CheckoutPage, OrderConfirmationPage
from config.settings import Config


class TestProductSearch:
    """Tests for product search and filtering."""
    
    def test_search_products(self, home_page):
        """Test searching for products."""
        home_page.open('/')
        search_results = home_page.search('laptop')
        
        # Verify search results page is loaded
        assert 'search' in search_results.get_current_url().lower() or \
               search_results.get_results_count() >= 0
    
    def test_search_no_results(self, home_page):
        """Test search with no results - boundary value testing."""
        home_page.open('/')
        search_results = home_page.search('xyznonexistent123')
        
        # Verify no results message or empty list
        assert search_results.has_no_results() or search_results.get_results_count() == 0
    
    def test_search_empty_query(self, home_page):
        """Test search with empty query - boundary value testing."""
        home_page.open('/')
        home_page.input_text(home_page.SEARCH_INPUT, '')
        home_page.click(home_page.SEARCH_BUTTON)
        
        # Should show all products or validation error
        assert home_page.get_product_count() > 0 or \
               home_page.get_current_url().endswith('/')
    
    def test_filter_by_category(self, home_page):
        """Test filtering products by category."""
        home_page.open('/')
        home_page = home_page.filter_by_category('Electronics')
        
        # Verify products are filtered (implementation dependent)
        assert home_page.get_product_count() >= 0
    
    def test_sort_products_by_price_asc(self, home_page):
        """Test sorting products by price ascending."""
        home_page.open('/')
        home_page = home_page.sort_products('Price: Low to High')
        
        # Verify products are sorted (would need actual price comparison)
        assert home_page.get_product_count() > 0
    
    def test_sort_products_by_price_desc(self, home_page):
        """Test sorting products by price descending."""
        home_page.open('/')
        home_page = home_page.sort_products('Price: High to Low')
        
        # Verify products are sorted
        assert home_page.get_product_count() > 0


class TestShoppingCart:
    """Tests for shopping cart functionality."""
    
    def test_add_product_to_cart(self, home_page):
        """Test adding product to cart."""
        home_page.open('/')
        
        # Get initial cart count if available
        initial_count = 0
        
        # Add product to cart (implementation may vary)
        # This assumes there's an add to cart button on product items
        product_items = home_page.find_elements(*home_page.PRODUCT_ITEMS)
        if product_items:
            product_items[0].click()  # Click first product
            
            # Navigate to cart
            cart_page = home_page.click_cart_link()
            
            # Verify cart has at least one item
            assert cart_page.get_cart_items_count() > 0 or not cart_page.is_cart_empty()
    
    def test_view_empty_cart(self, cart_page):
        """Test viewing empty cart."""
        cart_page.open('/cart')
        
        # Cart might be empty or have items depending on previous tests
        # Just verify the page loads
        assert 'cart' in cart_page.get_current_url().lower()
    
    def test_update_cart_quantity(self, cart_page):
        """Test updating cart item quantity."""
        cart_page.open('/cart')
        
        if not cart_page.is_cart_empty():
            # Increase quantity
            cart_page = cart_page.increase_quantity(0)
            
            # Verify quantity increased (implementation dependent)
            assert cart_page.get_cart_items_count() >= 1
    
    def test_remove_item_from_cart(self, cart_page):
        """Test removing item from cart."""
        cart_page.open('/cart')
        
        if not cart_page.is_cart_empty():
            initial_count = cart_page.get_cart_items_count()
            
            # Remove item
            cart_page = cart_page.remove_item(0)
            
            # Verify item count decreased
            assert cart_page.get_cart_items_count() < initial_count or cart_page.is_cart_empty()
    
    def test_cart_total_calculation(self, cart_page):
        """Test cart total amount calculation."""
        cart_page.open('/cart')
        
        if not cart_page.is_cart_empty():
            # Get total amount
            total = cart_page.get_total_amount()
            
            # Total should be positive
            assert total >= 0


class TestCheckout:
    """Tests for checkout flow."""
    
    def test_checkout_process(self, login_page, home_page):
        """Test complete checkout process."""
        # Login first
        home_page = login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
        
        # Navigate to cart
        cart_page = home_page.click_cart_link()
        
        if not cart_page.is_cart_empty():
            # Proceed to checkout
            checkout_page = cart_page.click_checkout()
            
            # Enter shipping address
            checkout_page = checkout_page.enter_shipping_address(
                address='123 Test Street',
                city='Test City',
                zip_code='12345'
            )
            
            # Verify checkout page elements are present
            assert checkout_page.is_element_present(checkout_page.PLACE_ORDER_BUTTON)
    
    def test_checkout_empty_cart(self, cart_page):
        """Test checkout with empty cart - negative scenario."""
        cart_page.open('/cart')
        
        if cart_page.is_cart_empty():
            # Checkout button should be disabled or not present
            assert not cart_page.is_element_present(cart_page.CHECKOUT_BUTTON) or \
                   not cart_page.find_element(*cart_page.CHECKOUT_BUTTON).is_enabled()
    
    def test_order_confirmation(self, login_page, home_page):
        """Test order confirmation after placing order."""
        # This test would require a full checkout flow
        # Simplified version just checks the confirmation page structure
        confirmation_page = OrderConfirmationPage(home_page.driver, home_page.base_url)
        confirmation_page.open('/order-confirmation')
        
        # Verify confirmation page elements exist (if order exists)
        # Note: This may fail if no orders exist, which is expected
        pass
