namespace Simanis62.Models;

/// <summary>
/// Model untuk data user.
/// </summary>
public class User
{
    public Guid Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string NamaLengkap { get; set; } = string.Empty;
    public string Role { get; set; } = "Viewer";
    public bool DapatEkspor { get; set; }
    public string Status { get; set; } = "Aktif";
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    /// <summary>
    /// Check if user is Admin.
    /// </summary>
    public bool IsAdmin => Role == "Admin";

    /// <summary>
    /// Check if user can export (Admin or Viewer with dapat_ekspor=true).
    /// </summary>
    public bool CanExport => IsAdmin || DapatEkspor;
}

/// <summary>
/// Request untuk login.
/// </summary>
public class LoginRequest
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

/// <summary>
/// Response dari login.
/// </summary>
public class LoginResponse
{
    public User User { get; set; } = new();
    public string Message { get; set; } = string.Empty;
}
