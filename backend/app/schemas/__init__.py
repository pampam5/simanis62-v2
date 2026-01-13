"""Schemas package untuk SIMANIS62 V2.

Package ini berisi:
- Response schemas (SuccessResponse, ErrorResponse, PaginatedResponse)
- Auth schemas (LoginRequest, UserResponse, etc.)
- Aset schemas (AsetCreate, AsetUpdate, AsetResponse)
- Mutasi schemas (MutasiCreate, MutasiResponse)
- User schemas (UserCreate, UserUpdate)
"""

# Response schemas
from .response import ErrorResponse, PaginatedResponse, SuccessResponse

# Aset schemas
from .aset import (
    AsetBase,
    AsetCreate,
    AsetResponse,
    AsetUpdate,
)

# Mutasi schemas
from .mutasi import (
    MutasiCreate,
    MutasiResponse,
)

# User schemas
from .user import (
    LoginRequest,
    UserCreate,
    UserResponse,
    UserUpdate,
)

__all__ = [
    # Response
    "ErrorResponse",
    "PaginatedResponse",
    "SuccessResponse",
    # Aset
    "AsetBase",
    "AsetCreate",
    "AsetResponse",
    "AsetUpdate",
    # Mutasi
    "MutasiCreate",
    "MutasiResponse",
    # User
    "LoginRequest",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
]
