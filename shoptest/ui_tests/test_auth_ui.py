import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage, RegisterPage
from pages.home_page import HomePage
from config.settings import Config


class TestRegistration:
    """Tests for user registration UI flow."""
    
    def test_register_new_user(self, login_page):
        """Test successful user registration."""
        # Navigate to registration page
        register_page = login_page.click_register_link()
        
        # Fill registration form
        register_page = register_page.register(
            username=f"testuser_{pytest.test_id}",
            email=f"test_{pytest.test_id}@example.com",
            password="TestPassword123!",
            confirm_password="TestPassword123!"
        )
        
        # Verify success message or redirect
        assert register_page.get_current_url() != register_page.base_url + '/register'
    
    def test_register_with_existing_email(self, login_page):
        """Test registration with existing email - negative scenario."""
        register_page = login_page.click_register_link()
        
        # Try to register with existing email
        register_page.register(
            username="existinguser",
            email=Config.TEST_EMAIL,
            password="TestPassword123!"
        )
        
        # Verify error message is displayed
        assert register_page.is_element_present(register_page.ERROR_MESSAGE)
    
    def test_register_password_mismatch(self, login_page):
        """Test registration with mismatched passwords - boundary value testing."""
        register_page = login_page.click_register_link()
        
        # Register with mismatched passwords
        register_page.register(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            confirm_password="DifferentPassword456!"
        )
        
        # Should show error or not submit
        assert register_page.is_element_present(register_page.ERROR_MESSAGE) or \
               register_page.get_current_url().endswith('/register')
    
    def test_register_weak_password(self, login_page):
        """Test registration with weak password - boundary value testing."""
        register_page = login_page.click_register_link()
        
        # Try to register with weak password
        register_page.register(
            username="testuser",
            email="test@example.com",
            password="123"  # Too short
        )
        
        # Should show validation error
        assert register_page.is_element_present(register_page.ERROR_MESSAGE)
    
    def test_register_empty_fields(self, login_page):
        """Test registration with empty required fields - negative scenario."""
        register_page = login_page.click_register_link()
        
        # Try to submit empty form
        register_page.click(register_page.REGISTER_BUTTON)
        
        # Should show validation errors
        assert register_page.is_element_present(register_page.ERROR_MESSAGE) or \
               register_page.get_current_url().endswith('/register')


class TestLogin:
    """Tests for user login UI flow."""
    
    def test_login_success(self, login_page):
        """Test successful login."""
        home_page = login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
        
        # Verify user is logged in
        assert home_page.is_user_logged_in()
        assert 'login' not in home_page.get_current_url().lower()
    
    def test_login_invalid_credentials(self, login_page):
        """Test login with invalid credentials - negative scenario."""
        login_page.open('/login')
        login_page.input_text(login_page.EMAIL_INPUT, 'invalid@example.com')
        login_page.input_text(login_page.PASSWORD_INPUT, 'WrongPassword123!')
        login_page.click(login_page.LOGIN_BUTTON)
        
        # Verify error message is displayed
        assert login_page.is_element_present(login_page.ERROR_MESSAGE)
    
    def test_login_empty_email(self, login_page):
        """Test login with empty email - boundary value testing."""
        login_page.open('/login')
        login_page.input_text(login_page.EMAIL_INPUT, '')
        login_page.input_text(login_page.PASSWORD_INPUT, 'TestPassword123!')
        login_page.click(login_page.LOGIN_BUTTON)
        
        # Should show validation error or not submit
        assert login_page.get_current_url().endswith('/login')
    
    def test_login_empty_password(self, login_page):
        """Test login with empty password - boundary value testing."""
        login_page.open('/login')
        login_page.input_text(login_page.EMAIL_INPUT, Config.TEST_EMAIL)
        login_page.input_text(login_page.PASSWORD_INPUT, '')
        login_page.click(login_page.LOGIN_BUTTON)
        
        # Should show validation error or not submit
        assert login_page.get_current_url().endswith('/login')
    
    def test_login_forgot_password_link(self, login_page):
        """Test forgot password link is present."""
        login_page.open('/login')
        
        # Verify forgot password link exists
        assert login_page.is_element_present(login_page.FORGOT_PASSWORD_LINK)
    
    def test_login_redirect_to_register(self, login_page):
        """Test redirect from login to register page."""
        login_page.open('/login')
        register_page = login_page.click_register_link()
        
        # Verify redirected to register page
        assert 'register' in register_page.get_current_url().lower()
    
    def test_logout(self, login_page):
        """Test user logout."""
        # Login first
        home_page = login_page.login(Config.TEST_EMAIL, Config.TEST_PASSWORD)
        assert home_page.is_user_logged_in()
        
        # Logout
        home_page.click_logout()
        
        # Verify user is logged out
        assert not home_page.is_user_logged_in()
