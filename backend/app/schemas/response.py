"""
Standard response schemas untuk SIMANIS62 V2 API.

Menyediakan response structure yang konsisten untuk semua endpoints.
"""

from typing import Any, ClassVar, Generic, TypeVar

from pydantic import BaseModel, Field

# Generic type untuk response data
T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response.

    Digunakan untuk semua response yang berhasil dengan data.

    Example:
        ```python
        return SuccessResponse(data=asset, message="Aset berhasil ditambahkan")
        ```
    """

    success: bool = Field(default=True, description="Status response")
    data: T = Field(..., description="Response data")
    message: str | None = Field(default=None, description="Optional success message")
    correlation_id: str | None = Field(
        default=None, description="Request correlation ID"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "success": True,
                "data": {"id": "123", "nama": "Komputer"},
                "message": "Data berhasil diambil",
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response.

    Digunakan untuk semua error response dari middleware atau exception handlers.

    Example:
        ```python
        return ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Kode barang tidak valid",
            details={"field": "kode_barang"},
        )
        ```
    """

    success: bool = Field(default=False, description="Status response")
    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(
        default=None, description="Additional error context"
    )
    correlation_id: str | None = Field(
        default=None, description="Request correlation ID"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "success": False,
                "error_code": "VALIDATION_ERROR",
                "message": "Format kode barang tidak valid",
                "details": {
                    "field": "kode_barang",
                    "expected_format": "XX.XX.XX.XXXX",
                },
                "correlation_id": "abc-123-def",
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response untuk list endpoints.

    Digunakan untuk endpoints yang mengembalikan list data dengan pagination.

    Example:
        ```python
        return PaginatedResponse(
            data=assets, total=150, page=1, page_size=100, total_pages=2
        )
        ```
    """

    success: bool = Field(default=True, description="Status response")
    data: list[T] = Field(..., description="List of items")
    total: int = Field(..., ge=0, description="Total items across all pages")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, le=1000, description="Number of items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    correlation_id: str | None = Field(
        default=None, description="Request correlation ID"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "success": True,
                "data": [
                    {"id": "1", "nama": "Item 1"},
                    {"id": "2", "nama": "Item 2"},
                ],
                "total": 150,
                "page": 1,
                "page_size": 100,
                "total_pages": 2,
            }
        }


class MessageResponse(BaseModel):
    """Simple response dengan hanya message.

    Digunakan untuk operasi yang tidak perlu return data (seperti delete).

    Example:
        ```python
        return MessageResponse(message="Aset berhasil dihapus")
        ```
    """

    success: bool = Field(default=True, description="Status response")
    message: str = Field(..., description="Response message")
    correlation_id: str | None = Field(
        default=None, description="Request correlation ID"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "success": True,
                "message": "Operasi berhasil dilakukan",
            }
        }


class HealthResponse(BaseModel):
    """Response untuk health check endpoint.

    Example:
        ```python
        return HealthResponse(
            status="healthy",
            version="2.0.0",
            database={"status": "healthy", "journal_mode": "WAL"},
        )
        ```
    """

    status: str = Field(..., description="Overall health status")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment name")
    database: dict[str, Any] = Field(..., description="Database health info")
    timestamp: str = Field(..., description="Response timestamp")

    class Config:
        """Pydantic config."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "status": "healthy",
                "version": "2.0.0",
                "environment": "production",
                "database": {
                    "status": "healthy",
                    "journal_mode": "WAL",
                    "integrity": "ok",
                },
                "timestamp": "2026-01-11T15:00:00Z",
            }
        }
