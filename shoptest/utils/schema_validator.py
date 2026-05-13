from jsonschema import validate, ValidationError
from typing import Dict, Any


class SchemaValidator:
    """JSON Schema validator for API responses."""
    
    @staticmethod
    def validate_schema(response_data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate response data against JSON schema.
        
        Args:
            response_data: The data to validate
            schema: The JSON schema to validate against
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            validate(instance=response_data, schema=schema)
            return True
        except ValidationError as e:
            raise ValidationError(f"Schema validation failed: {e.message}")
    
    @staticmethod
    def validate_status_code(actual_status: int, expected_status: int) -> bool:
        """Validate HTTP status code."""
        assert actual_status == expected_status, \
            f"Expected status code {expected_status}, got {actual_status}"
        return True
    
    @staticmethod
    def validate_response_time(response_time: float, max_time: float = 5.0) -> bool:
        """Validate response time is within acceptable limits."""
        assert response_time <= max_time, \
            f"Response time {response_time}s exceeds maximum {max_time}s"
        return True
