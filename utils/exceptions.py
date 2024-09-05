from uuid import UUID

import uuid_utils as uuid


def get_error_id() -> UUID:
    """Generate a unique error UUID for logging."""
    return uuid.uuid7()

class ClientInitializationError(RuntimeError):
    """Exception raised when the Supabase client is not initialized."""
