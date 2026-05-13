import requests
from typing import Optional, Dict, Any


class APIClient:
    """Base API client for making HTTP requests."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.token: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get default headers with authentication if token exists."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def set_token(self, token: str) -> None:
        """Set authentication token."""
        self.token = token
    
    def clear_token(self) -> None:
        """Clear authentication token."""
        self.token = None
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs
        )
        return response
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make GET request."""
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Make POST request."""
        return self.request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Make PUT request."""
        return self.request('PUT', endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """Make PATCH request."""
        return self.request('PATCH', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request."""
        return self.request('DELETE', endpoint, **kwargs)
