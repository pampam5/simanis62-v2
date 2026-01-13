"""
Security utilities untuk SIMANIS62 V2.

Menyediakan password hashing dan verification.
Menggunakan bcrypt langsung untuk menghindari konflik passlib/bcrypt 4.x.
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt.

    Args:
        password: Plain text password (max 72 bytes untuk bcrypt)

    Returns:
        Hashed password
    """
    # Encode password ke bytes, truncate ke 72 bytes (bcrypt limit)
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    try:
        password_bytes = plain_password.encode("utf-8")[:72]
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def revoke_all_user_sessions(user_id) -> None:
    """Revoke all sessions for a user.

    This is a synchronous wrapper that clears sessions from the in-memory store.
    For production, this should be moved to database-based session management.

    Args:
        user_id: User ID (UUID or string)
    """
    from app.core.auth import _sessions
    
    # Convert to string for comparison if needed
    user_id_str = str(user_id)
    
    # Remove all sessions for this user
    sessions_to_remove = [
        sid for sid, (uid, _) in _sessions.items() 
        if str(uid) == user_id_str
    ]
    for sid in sessions_to_remove:
        del _sessions[sid]
