namespace Simanis62.Core.Exceptions;

/// <summary>
/// Base exception untuk semua error SIMANIS62.
/// </summary>
public class SimanisException : Exception
{
    public string ErrorCode { get; }
    public Dictionary<string, object>? Details { get; }

    public SimanisException(string message, string errorCode, Dictionary<string, object>? details = null)
        : base(message)
    {
        ErrorCode = errorCode;
        Details = details;
    }
}

/// <summary>
/// Error koneksi ke API.
/// </summary>
public class ApiConnectionException : SimanisException
{
    public ApiConnectionException(string message = "Tidak dapat terhubung ke server")
        : base(message, "API_CONNECTION_ERROR") { }
}

/// <summary>
/// Error autentikasi.
/// </summary>
public class AuthenticationException : SimanisException
{
    public AuthenticationException(string message = "Autentikasi gagal")
        : base(message, "AUTH_ERROR") { }
}

/// <summary>
/// Session expired.
/// </summary>
public class SessionExpiredException : SimanisException
{
    public SessionExpiredException()
        : base("Session telah berakhir, silakan login kembali", "SESSION_EXPIRED") { }
}

/// <summary>
/// Error otorisasi.
/// </summary>
public class AuthorizationException : SimanisException
{
    public AuthorizationException(string message = "Akses ditolak")
        : base(message, "AUTHZ_ERROR") { }
}

/// <summary>
/// Error validasi.
/// </summary>
public class ValidationException : SimanisException
{
    public string Field { get; }

    public ValidationException(string message, string field)
        : base(message, "VALIDATION_ERROR", new Dictionary<string, object> { { "field", field } })
    {
        Field = field;
    }
}

/// <summary>
/// Resource tidak ditemukan.
/// </summary>
public class NotFoundException : SimanisException
{
    public NotFoundException(string resourceType, string resourceId)
        : base($"{resourceType} dengan ID '{resourceId}' tidak ditemukan", "NOT_FOUND",
            new Dictionary<string, object> { { "resource_type", resourceType }, { "resource_id", resourceId } }) { }
}
