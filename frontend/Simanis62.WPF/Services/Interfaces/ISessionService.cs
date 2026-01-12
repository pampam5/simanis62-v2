using Simanis62.Models;

namespace Simanis62.Services.Interfaces;

/// <summary>
/// Service untuk mengelola session user.
/// </summary>
public interface ISessionService
{
    /// <summary>
    /// Current logged in user.
    /// </summary>
    User? CurrentUser { get; }

    /// <summary>
    /// Check if user is logged in.
    /// </summary>
    bool IsLoggedIn { get; }

    /// <summary>
    /// Check if current user is Admin.
    /// </summary>
    bool IsAdmin { get; }

    /// <summary>
    /// Check if current user can export.
    /// </summary>
    bool CanExport { get; }

    /// <summary>
    /// Event when session changes.
    /// </summary>
    event Action? SessionChanged;

    /// <summary>
    /// Set current user after login.
    /// </summary>
    void SetUser(User user);

    /// <summary>
    /// Clear session on logout.
    /// </summary>
    void ClearSession();
}
