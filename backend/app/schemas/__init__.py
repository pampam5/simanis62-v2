"""Schemas package untuk SIMANIS62 V2.

Package ini berisi:
- Response schemas (SuccessResponse, ErrorResponse, PaginatedResponse)
- Auth schemas (LoginRequest, LoginResponse, UserResponse, etc.)
- Aset schemas (AsetCreate, AsetUpdate, AsetResponse, KIB-specific schemas)
- Mutasi schemas (MutasiCreate, MutasiResponse, MutasiCancelRequest)
- KIB schemas (KibReportResponse, KibExportRequest)
- User schemas (UserCreate, UserUpdate, UserSearchParams)
"""

# Response schemas
# Aset schemas
from .aset import (
    AsetBase,
    AsetCreate,
    AsetCreateKIBA,
    AsetCreateKIBB,
    AsetCreateKIBC,
    AsetCreateKIBD,
    AsetCreateKIBE,
    AsetCreateKIBF,
    AsetDeleteRequest,
    AsetResponse,
    AsetSearchParams,
    AsetUpdate,
    KIBAFields,
    KIBBFields,
    KIBCFields,
    KIBDFields,
    KIBEFields,
    KIBFFields,
)

# Auth schemas
from .auth import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    SessionInfo,
    UserResponse,
)

# KIB schemas
from .kib import (
    KibAItem,
    KibBItem,
    KibCItem,
    KibDItem,
    KibEItem,
    KibExportRequest,
    KibExportResponse,
    KibFItem,
    KibItemBase,
    KibReportResponse,
    KibSummary,
)

# Mutasi schemas
from .mutasi import (
    AsetBrief,
    MutasiCancelRequest,
    MutasiCompleteRequest,
    MutasiCreate,
    MutasiResponse,
    MutasiSearchParams,
    RuanganBrief,
    UserBrief,
)
from .response import ErrorResponse, PaginatedResponse, SuccessResponse

# User schemas
from .user import (
    UserCreate,
    UserDeactivateRequest,
    UserSearchParams,
    UserUpdate,
)

__all__ = [
    # Aset
    "AsetBase",
    # Mutasi
    "AsetBrief",
    "AsetCreate",
    "AsetCreateKIBA",
    "AsetCreateKIBB",
    "AsetCreateKIBC",
    "AsetCreateKIBD",
    "AsetCreateKIBE",
    "AsetCreateKIBF",
    "AsetDeleteRequest",
    "AsetResponse",
    "AsetSearchParams",
    "AsetUpdate",
    # Response
    "ErrorResponse",
    "KIBAFields",
    "KIBBFields",
    "KIBCFields",
    "KIBDFields",
    "KIBEFields",
    "KIBFFields",
    # KIB
    "KibAItem",
    "KibBItem",
    "KibCItem",
    "KibDItem",
    "KibEItem",
    "KibExportRequest",
    "KibExportResponse",
    "KibFItem",
    "KibItemBase",
    "KibReportResponse",
    "KibSummary",
    # Auth
    "LoginRequest",
    "LoginResponse",
    "LogoutResponse",
    "MutasiCancelRequest",
    "MutasiCompleteRequest",
    "MutasiCreate",
    "MutasiResponse",
    "MutasiSearchParams",
    "PaginatedResponse",
    "RuanganBrief",
    "SessionInfo",
    "SuccessResponse",
    "UserBrief",
    # User
    "UserCreate",
    "UserDeactivateRequest",
    "UserResponse",
    "UserSearchParams",
    "UserUpdate",
]
