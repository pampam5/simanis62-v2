"""Schemas package untuk SIMANIS62 V2.

Package ini berisi:
- Response schemas (SuccessResponse, ErrorResponse, PaginatedResponse)
- Request/Response models untuk API endpoints
"""

from .response import ErrorResponse, PaginatedResponse, SuccessResponse

__all__ = [
    "ErrorResponse",
    "PaginatedResponse",
    "SuccessResponse",
]
