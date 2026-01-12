"""
Security utilities untuk SIMANIS62 V2.

Menyediakan password hashing dengan bcrypt dan session management
berbasis in-memory store dengan automatic expiration.
"""

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context menggunakan bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory session store with session_token as key
# Each session contains user_id and expires_at timestamp
_sessions: dict[str, dict[str, Any]] = {}


def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password

    Example:
        ```python
        hashed = hash_password("password123")
        # Returns: "$2b$12$..."
        ```
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password terhadap hash.

    Args:
        plain_password: Plain text password dari user
        hashed_password: Hashed password dari database

    Returns:
        bool: True jika password cocok, False jika tidak

    Example:
        ```python
        is_valid = verify_password("password123", hashed_from_db)
        ```
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_session(user_id: str) -> str:
    """Create new session untuk user.

    Args:
        user_id: UUID user yang login

    Returns:
        str: Session token (32 bytes random hex)

    Example:
        ```python
        session_token = create_session(str(user.id))
        # Returns: "a1b2c3d4..."
        ```
    """
    # Generate secure random token
    session_token = secrets.token_hex(32)

    # Calculate expiration time
    expires_at = datetime.now(UTC) + timedelta(hours=settings.session_timeout_hours)

    # Store session
    _sessions[session_token] = {
        "user_id": user_id,
        "expires_at": expires_at,
        "created_at": datetime.now(UTC),
    }

    return session_token


def verify_session(session_token: str) -> str | None:
    """Verify session token dan return user_id jika valid.

    Args:
        session_token: Session token dari cookie

    Returns:
        str | None: User ID jika session valid, None jika invalid/expired

    Example:
        ```python
        user_id = verify_session(token_from_cookie)
        if user_id:
            # Session valid
            pass
        else:
            # Session invalid atau expired
            pass
        ```
    """
    session = _sessions.get(session_token)

    if session is None:
        return None

    # Check expiration
    if datetime.now(UTC) > session["expires_at"]:
        # Session expired, remove it
        destroy_session(session_token)
        return None

    return session["user_id"]


def destroy_session(session_token: str) -> bool:
    """Destroy session (logout).

    Args:
        session_token: Session token yang akan dihapus

    Returns:
        bool: True jika session ditemukan dan dihapus, False jika tidak ada

    Example:
        ```python
        destroyed = destroy_session(token_from_cookie)
        if destroyed:
            # Session berhasil dihapus
            pass
        ```
    """
    if session_token in _sessions:
        del _sessions[session_token]
        return True
    return False


def cleanup_expired_sessions() -> int:
    """Cleanup expired sessions dari memory.

    Returns:
        int: Jumlah session yang dihapus

    Note:
        Function ini sebaiknya dipanggil secara periodic
        (misalnya setiap jam via background task).
    """
    now = datetime.now(UTC)
    expired_tokens = [
        token for token, session in _sessions.items() if now > session["expires_at"]
    ]

    for token in expired_tokens:
        del _sessions[token]

    return len(expired_tokens)


def get_active_sessions_count() -> int:
    """Get jumlah active sessions.

    Returns:
        int: Jumlah session yang masih valid
    """
    now = datetime.now(UTC)
    return sum(1 for session in _sessions.values() if now <= session["expires_at"])


def get_user_sessions(user_id: str) -> list[str]:
    """Get semua session tokens untuk user tertentu.

    Args:
        user_id: User ID

    Returns:
        list[str]: List of session tokens

    Example:
        ```python
        tokens = get_user_sessions(str(user.id))
        # Bisa digunakan untuk force logout user dari semua devices
        ```
    """
    return [
        token for token, session in _sessions.items() if session["user_id"] == user_id
    ]


def revoke_all_user_sessions(user_id: str) -> int:
    """Revoke semua session untuk user tertentu.

    Args:
        user_id: User ID

    Returns:
        int: Jumlah session yang di-revoke

    Example:
        ```python
        # Force logout user dari semua devices
        count = revoke_all_user_sessions(str(user.id))
        ```
    """
    tokens = get_user_sessions(user_id)
    for token in tokens:
        del _sessions[token]
    return len(tokens)


def generate_secure_token(length: int = 32) -> str:
    """Generate secure random token.

    Args:
        length: Length dalam bytes (default 32 = 64 hex chars)

    Returns:
        str: Random hex token

    Example:
        ```python
        reset_token = generate_secure_token(16)
        # Returns 32 character hex string
        ```
    """
    return secrets.token_hex(length)
