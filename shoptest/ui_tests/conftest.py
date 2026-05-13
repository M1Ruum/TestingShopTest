import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import Config


@pytest.fixture(scope='session')
def driver():
    """Create and yield WebDriver instance."""
    chrome_options = Options()
    
    if Config.HEADLESS:
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


@pytest.fixture
def login_page(driver):
    """Create LoginPage instance."""
    from pages.login_page import LoginPage
    return LoginPage(driver, Config.UI_BASE_URL)


@pytest.fixture
def home_page(driver):
    """Create HomePage instance."""
    from pages.home_page import HomePage
    return HomePage(driver, Config.UI_BASE_URL)


@pytest.fixture
def cart_page(driver):
    """Create CartPage instance."""
    from pages.cart_page import CartPage
    return CartPage(driver, Config.UI_BASE_URL)
