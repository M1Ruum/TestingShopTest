from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object."""
    
    # Locators
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    REGISTER_LINK = (By.LINK_TEXT, 'Register')
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, 'Forgot Password?')
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message')
    
    def login(self, email: str, password: str) -> 'HomePage':
        """Login with credentials."""
        self.open('/login')
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        from pages.home_page import HomePage
        return HomePage(self.driver, self.base_url)
    
    def click_register_link(self) -> 'RegisterPage':
        """Click on register link."""
        self.click(self.REGISTER_LINK)
        from pages.register_page import RegisterPage
        return RegisterPage(self.driver, self.base_url)
    
    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_login_button_displayed(self) -> bool:
        """Check if login button is displayed."""
        return self.is_element_present(self.LOGIN_BUTTON)


class RegisterPage(BasePage):
    """Registration page object."""
    
    # Locators
    USERNAME_INPUT = (By.ID, 'username')
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    CONFIRM_PASSWORD_INPUT = (By.ID, 'confirm_password')
    REGISTER_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    LOGIN_LINK = (By.LINK_TEXT, 'Login')
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message')
    SUCCESS_MESSAGE = (By.CLASS_NAME, 'success-message')
    
    def register(self, username: str, email: str, password: str, confirm_password: str = None) -> 'BasePage':
        """Register new user."""
        self.open('/register')
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
        
        if confirm_password:
            self.input_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        
        self.click(self.REGISTER_BUTTON)
        return self
    
    def click_login_link(self) -> LoginPage:
        """Click on login link."""
        self.click(self.LOGIN_LINK)
        return LoginPage(self.driver, self.base_url)
    
    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_success_message(self) -> str:
        """Get success message text."""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def is_register_button_displayed(self) -> bool:
        """Check if register button is displayed."""
        return self.is_element_present(self.REGISTER_BUTTON)
