"""Models package untuk SIMANIS62 V2.

Package ini berisi SQLModel entities untuk database:
- User: Authentication dan authorization
- Ruangan: Room/location management
- Aset: Main asset table (all KIB types)
- AsetKIBA-F: KIB-specific extension tables
- RiwayatMutasi: Asset movement history
- AuditTrail: Complete audit log
"""

from .aset import (
    AsalUsul,
    Aset,
    KategoriKIB,
    Kondisi,
    StatusAset,
)
from .aset_kib import (
    AsetKIBA,
    AsetKIBB,
    AsetKIBC,
    AsetKIBD,
    AsetKIBE,
    AsetKIBF,
)
from .audit import AuditTrail, Operation
from .base import BaseModel, TimestampMixin
from .mutasi import RiwayatMutasi, StatusMutasi
from .ruangan import Ruangan
from .user import User, UserRole, UserStatus

__all__ = [
    "AsalUsul",
    # Aset
    "Aset",
    # KIB Extensions
    "AsetKIBA",
    "AsetKIBB",
    "AsetKIBC",
    "AsetKIBD",
    "AsetKIBE",
    "AsetKIBF",
    # Audit
    "AuditTrail",
    # Base
    "BaseModel",
    "KategoriKIB",
    "Kondisi",
    "Operation",
    # Mutasi
    "RiwayatMutasi",
    # Ruangan
    "Ruangan",
    "StatusAset",
    "StatusMutasi",
    "TimestampMixin",
    # User
    "User",
    "UserRole",
    "UserStatus",
]
