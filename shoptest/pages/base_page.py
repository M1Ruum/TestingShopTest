from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional


class BasePage:
    """Base page class with common methods."""
    
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 30)
    
    def open(self, path: str = '') -> 'BasePage':
        """Open page by path."""
        self.driver.get(f"{self.base_url}{path}")
        return self
    
    def find_element(self, by: By, value: str):
        """Find element on page."""
        return self.driver.find_element(by, value)
    
    def find_elements(self, by: By, value: str):
        """Find multiple elements on page."""
        return self.driver.find_elements(by, value)
    
    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """Wait for element to be present."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def wait_for_element_clickable(self, by: By, value: str, timeout: int = 10):
        """Wait for element to be clickable."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def wait_for_element_visible(self, by: By, value: str, timeout: int = 10):
        """Wait for element to be visible."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))
    
    def click(self, by: By, value: str) -> None:
        """Click on element."""
        element = self.wait_for_element_clickable(by, value)
        element.click()
    
    def input_text(self, by: By, value: str, text: str) -> None:
        """Input text into field."""
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, by: By, value: str) -> str:
        """Get text from element."""
        element = self.wait_for_element(by, value)
        return element.text
    
    def is_element_present(self, by: By, value: str) -> bool:
        """Check if element is present."""
        try:
            self.driver.find_element(by, value)
            return True
        except:
            return False
    
    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
    
    def accept_alert(self) -> None:
        """Accept alert."""
        alert = self.driver.switch_to.alert
        alert.accept()
    
    def dismiss_alert(self) -> None:
        """Dismiss alert."""
        alert = self.driver.switch_to.alert
        alert.dismiss()
