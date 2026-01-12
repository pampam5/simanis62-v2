using Simanis62.Models;
using Simanis62.Services.Interfaces;

namespace Simanis62.Services;

/// <summary>
/// Implementation of session service.
/// </summary>
public class SessionService : ISessionService
{
    public User? CurrentUser { get; private set; }
    public bool IsLoggedIn => CurrentUser != null;
    public bool IsAdmin => CurrentUser?.IsAdmin ?? false;
    public bool CanExport => CurrentUser?.CanExport ?? false;

    public event Action? SessionChanged;

    public void SetUser(User user)
    {
        CurrentUser = user;
        SessionChanged?.Invoke();
    }

    public void ClearSession()
    {
        CurrentUser = null;
        SessionChanged?.Invoke();
    }
}
