from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object."""
    
    # Locators
    SEARCH_INPUT = (By.ID, 'search')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button.search-btn')
    CART_LINK = (By.LINK_TEXT, 'Cart')
    LOGIN_LINK = (By.LINK_TEXT, 'Login')
    LOGOUT_LINK = (By.LINK_TEXT, 'Logout')
    PRODUCT_LIST = (By.CLASS_NAME, 'product-list')
    PRODUCT_ITEMS = (By.CLASS_NAME, 'product-item')
    CATEGORY_FILTER = (By.ID, 'category-filter')
    SORT_DROPDOWN = (By.ID, 'sort-dropdown')
    USER_MENU = (By.CLASS_NAME, 'user-menu')
    
    def search(self, query: str) -> 'SearchResultsPage':
        """Search for products."""
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        from pages.search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver, self.base_url)
    
    def click_cart_link(self) -> 'CartPage':
        """Click on cart link."""
        self.click(self.CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver, self.base_url)
    
    def click_login_link(self) -> 'LoginPage':
        """Click on login link."""
        self.click(self.LOGIN_LINK)
        from pages.login_page import LoginPage
        return LoginPage(self.driver, self.base_url)
    
    def click_logout(self) -> 'HomePage':
        """Click on logout link."""
        self.click(self.LOGOUT_LINK)
        return self
    
    def get_product_count(self) -> int:
        """Get number of products displayed."""
        products = self.find_elements(*self.PRODUCT_ITEMS)
        return len(products)
    
    def filter_by_category(self, category: str) -> 'HomePage':
        """Filter products by category."""
        dropdown = self.wait_for_element(*self.CATEGORY_FILTER)
        dropdown.click()
        
        from selenium.webdriver.support.ui import Select
        select = Select(dropdown)
        select.select_by_visible_text(category)
        return self
    
    def sort_products(self, sort_option: str) -> 'HomePage':
        """Sort products."""
        dropdown = self.wait_for_element(*self.SORT_DROPDOWN)
        dropdown.click()
        
        from selenium.webdriver.support.ui import Select
        select = Select(dropdown)
        select.select_by_visible_text(sort_option)
        return self
    
    def is_user_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.is_element_present(self.USER_MENU) or self.is_element_present(self.LOGOUT_LINK)


class SearchResultsPage(BasePage):
    """Search results page object."""
    
    # Locators
    SEARCH_RESULTS = (By.CLASS_NAME, 'search-results')
    RESULT_ITEMS = (By.CLASS_NAME, 'result-item')
    NO_RESULTS_MESSAGE = (By.CLASS_NAME, 'no-results')
    
    def get_results_count(self) -> int:
        """Get number of search results."""
        items = self.find_elements(*self.RESULT_ITEMS)
        return len(items)
    
    def has_no_results(self) -> bool:
        """Check if no results message is displayed."""
        return self.is_element_present(self.NO_RESULTS_MESSAGE)
    
    def click_add_to_cart(self, product_index: int = 0) -> 'HomePage':
        """Add product to cart by index."""
        add_buttons = self.find_elements(*self.RESULT_ITEMS)
        if add_buttons:
            add_buttons[product_index].click()
        return HomePage(self.driver, self.base_url)
