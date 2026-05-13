# ShopTest - Internet Store Testing Framework

A comprehensive testing framework for web-based e-commerce applications combining API and UI testing.

## Project Structure

```
shoptest/
├── api_tests/              # API test cases
│   ├── __init__.py
│   ├── test_auth.py        # Authentication API tests
│   ├── test_products.py    # Products API tests
│   └── test_orders.py      # Orders API tests
├── ui_tests/               # UI test cases
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_auth_ui.py     # Authentication UI tests
│   └── test_shopping.py    # Shopping flow UI tests
├── pages/                  # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py        # Base page class
│   ├── login_page.py       # Login/Register pages
│   ├── home_page.py        # Home/Search pages
│   └── cart_page.py        # Cart/Checkout pages
├── utils/                  # Utility classes
│   ├── __init__.py
│   ├── api_client.py       # HTTP client wrapper
│   └── schema_validator.py # JSON Schema validator
├── schemas/                # JSON Schema definitions
│   ├── user_schema.json
│   ├── product_schema.json
│   └── order_schema.json
├── config/                 # Configuration
│   ├── __init__.py
│   └── settings.py         # Test configuration
├── test_data/              # Test data files
├── reports/                # Test reports
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Features

### API Testing
- REST API testing with `requests` library
- JWT token authentication
- JSON Schema validation
- Status code verification
- Response time validation
- Positive and negative test scenarios
- Boundary value testing

### UI Testing
- Selenium WebDriver automation
- Page Object Model (POM) pattern
- Explicit and implicit waits
- Form handling
- Dropdown interactions
- Alert handling
- Full user journey testing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd shoptest
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root:
```env
API_BASE_URL=http://localhost:8000/api/v1
UI_BASE_URL=http://localhost:3000
TEST_EMAIL=test@example.com
TEST_PASSWORD=TestPassword123!
BROWSER=chrome
HEADLESS=false
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run API tests only:
```bash
pytest api_tests/ -v
```

### Run UI tests only:
```bash
pytest ui_tests/ -v
```

### Run specific test file:
```bash
pytest api_tests/test_auth.py -v
```

### Run with HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run with Allure report:
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Run in headless mode:
```bash
HEADLESS=true pytest ui_tests/ -v
```

## Test Categories

### API Tests
- **Authentication**: Registration, login, token validation
- **Products**: CRUD operations, filtering, sorting
- **Orders**: Order creation, status updates, cancellation

### UI Tests
- **Registration**: New user registration, validation
- **Login**: Authentication, error handling, logout
- **Search**: Product search, filtering, sorting
- **Cart**: Add/remove items, quantity updates
- **Checkout**: Order placement, confirmation

## Configuration

Edit `config/settings.py` or environment variables to customize:

- API and UI base URLs
- Browser settings (Chrome/Firefox)
- Headless mode
- Wait timeouts
- Test credentials

## Extending the Framework

### Adding new API tests:
1. Create new test file in `api_tests/`
2. Use `APIClient` for HTTP requests
3. Use `SchemaValidator` for response validation

### Adding new Page Objects:
1. Create new page class in `pages/`
2. Extend `BasePage` class
3. Define locators as class constants
4. Implement page-specific methods

### Adding test data:
1. Place JSON/CSV files in `test_data/`
2. Load data in test fixtures or test methods

## Best Practices

- Use Page Object Model for UI tests
- Keep tests independent and isolated
- Use fixtures for common setup/teardown
- Validate both status codes and response schemas
- Include both positive and negative scenarios
- Use meaningful test names
- Clean up test data after tests

## Requirements

- Python 3.8+
- Chrome/Firefox browser
- Web application under test

## License

MIT License
