from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page object."""
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, 'cart-item')
    ITEM_QUANTITY = (By.CLASS_NAME, 'item-quantity')
    ITEM_PRICE = (By.CLASS_NAME, 'item-price')
    TOTAL_AMOUNT = (By.CLASS_NAME, 'total-amount')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, 'button.checkout-btn')
    REMOVE_BUTTON = (By.CLASS_NAME, 'remove-btn')
    EMPTY_CART_MESSAGE = (By.CLASS_NAME, 'empty-cart-message')
    QUANTITY_INCREASE = (By.CLASS_NAME, 'quantity-increase')
    QUANTITY_DECREASE = (By.CLASS_NAME, 'quantity-decrease')
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart."""
        items = self.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return self.is_element_present(self.EMPTY_CART_MESSAGE)
    
    def get_total_amount(self) -> float:
        """Get total amount from cart."""
        total_text = self.get_text(self.TOTAL_AMOUNT)
        # Remove currency symbol and parse
        return float(total_text.replace('$', '').replace(',', ''))
    
    def click_checkout(self) -> 'CheckoutPage':
        """Click checkout button."""
        self.click(self.CHECKOUT_BUTTON)
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver, self.base_url)
    
    def remove_item(self, item_index: int = 0) -> 'CartPage':
        """Remove item from cart by index."""
        remove_buttons = self.find_elements(*self.REMOVE_BUTTON)
        if remove_buttons:
            remove_buttons[item_index].click()
        return self
    
    def increase_quantity(self, item_index: int = 0) -> 'CartPage':
        """Increase item quantity."""
        increase_buttons = self.find_elements(*self.QUANTITY_INCREASE)
        if increase_buttons:
            increase_buttons[item_index].click()
        return self
    
    def decrease_quantity(self, item_index: int = 0) -> 'CartPage':
        """Decrease item quantity."""
        decrease_buttons = self.find_elements(*self.QUANTITY_DECREASE)
        if decrease_buttons:
            decrease_buttons[item_index].click()
        return self
    
    def update_quantity(self, item_index: int, quantity: int) -> 'CartPage':
        """Update item quantity directly."""
        quantity_inputs = self.find_elements(*self.ITEM_QUANTITY)
        if quantity_inputs:
            quantity_inputs[item_index].clear()
            quantity_inputs[item_index].send_keys(str(quantity))
        return self


class CheckoutPage(BasePage):
    """Checkout page object."""
    
    # Locators
    SHIPPING_ADDRESS_INPUT = (By.ID, 'shipping-address')
    CITY_INPUT = (By.ID, 'city')
    ZIP_CODE_INPUT = (By.ID, 'zip-code')
    PAYMENT_METHOD = (By.NAME, 'payment-method')
    CARD_NUMBER_INPUT = (By.ID, 'card-number')
    EXPIRY_DATE_INPUT = (By.ID, 'expiry-date')
    CVV_INPUT = (By.ID, 'cvv')
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, 'button.place-order-btn')
    ORDER_CONFIRMATION = (By.CLASS_NAME, 'order-confirmation')
    ORDER_NUMBER = (By.CLASS_NAME, 'order-number')
    
    def enter_shipping_address(self, address: str, city: str, zip_code: str) -> 'CheckoutPage':
        """Enter shipping address."""
        self.input_text(self.SHIPPING_ADDRESS_INPUT, address)
        self.input_text(self.CITY_INPUT, city)
        self.input_text(self.ZIP_CODE_INPUT, zip_code)
        return self
    
    def select_payment_method(self, method: str) -> 'CheckoutPage':
        """Select payment method."""
        self.click(self.PAYMENT_METHOD)
        # Implementation depends on dropdown type
        return self
    
    def enter_payment_details(self, card_number: str, expiry: str, cvv: str) -> 'CheckoutPage':
        """Enter payment details."""
        self.input_text(self.CARD_NUMBER_INPUT, card_number)
        self.input_text(self.EXPIRY_DATE_INPUT, expiry)
        self.input_text(self.CVV_INPUT, cvv)
        return self
    
    def place_order(self) -> 'OrderConfirmationPage':
        """Place order."""
        self.click(self.PLACE_ORDER_BUTTON)
        from pages.order_confirmation_page import OrderConfirmationPage
        return OrderConfirmationPage(self.driver, self.base_url)
    
    def is_order_confirmed(self) -> bool:
        """Check if order confirmation is displayed."""
        return self.is_element_present(self.ORDER_CONFIRMATION)
    
    def get_order_number(self) -> str:
        """Get order number from confirmation."""
        return self.get_text(self.ORDER_NUMBER)


class OrderConfirmationPage(BasePage):
    """Order confirmation page object."""
    
    # Locators
    CONFIRMATION_MESSAGE = (By.CLASS_NAME, 'confirmation-message')
    ORDER_NUMBER = (By.CLASS_NAME, 'order-number')
    ORDER_DETAILS = (By.CLASS_NAME, 'order-details')
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, 'button.continue-shopping-btn')
    
    def get_confirmation_message(self) -> str:
        """Get confirmation message."""
        return self.get_text(self.CONFIRMATION_MESSAGE)
    
    def get_order_number(self) -> str:
        """Get order number."""
        return self.get_text(self.ORDER_NUMBER)
    
    def click_continue_shopping(self) -> 'HomePage':
        """Click continue shopping button."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        from pages.home_page import HomePage
        return HomePage(self.driver, self.base_url)
