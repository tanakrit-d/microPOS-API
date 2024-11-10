# src/utils/exceptions.py
from __future__ import annotations

import uuid
from typing import Any


def get_error_id() -> str:
    """Generate a unique identifier for error tracking."""
    return str(uuid.uuid4())


class ClientInitializationError(Exception):
    """Raised when the Supabase client fails to initialize."""


class DataSeedingError(Exception):
    """Base exception for data seeding errors."""

    def __init__(
        self,
        message: str,
        error_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize the DataSeedingError.

        Args:
            message: The error message
            error_id: Unique identifier for error tracking
            details: Additional error context

        """
        self.error_id = error_id or get_error_id()
        self.details = details or {}
        super().__init__(f"Error ID: {self.error_id}; {message}")


class ItemSeedingError(DataSeedingError):
    """Raised when failing to seed menu items."""

    def __init__(
        self,
        message: str,
        item_data: dict[str, Any] | None = None,
        original_error: Exception | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the ItemSeedingError.

        Args:
            message: The error message
            item_data: The item data that failed to seed
            original_error: The original exception that caused this error
            **kwargs: Additional keyword arguments passed to DataSeedingError

        """
        details = kwargs.pop("details", {})
        if item_data:
            details["item_data"] = item_data
        if original_error:
            details["original_error"] = str(original_error)
            details["error_type"] = type(original_error).__name__

        super().__init__(message, details=details, **kwargs)


class ValidationSeedingError(ItemSeedingError):
    """Raised when generated data fails validation."""

    def __init__(
        self,
        field_name: str,
        invalid_value: Any,
        validation_error: Exception,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the ValidationSeedingError.

        Args:
            field_name: Name of the field that failed validation
            invalid_value: The value that failed validation
            validation_error: The validation error
            **kwargs: Additional keyword arguments passed to ItemSeedingError

        """
        details = kwargs.pop("details", {})
        details.update({
            "field_name": field_name,
            "invalid_value": str(invalid_value),
            "validation_error": str(validation_error),
        })

        message = f"Validation failed for field '{field_name}'"
        super().__init__(message, details=details, **kwargs)
