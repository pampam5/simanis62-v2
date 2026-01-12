namespace Simanis62.Services.Interfaces;

/// <summary>
/// Service untuk navigasi antar views.
/// </summary>
public interface INavigationService
{
    /// <summary>
    /// Current view name.
    /// </summary>
    string CurrentView { get; }

    /// <summary>
    /// Event when navigation changes.
    /// </summary>
    event Action<string>? NavigationChanged;

    /// <summary>
    /// Navigate to a view.
    /// </summary>
    void NavigateTo(string viewName, object? parameter = null);

    /// <summary>
    /// Navigate back.
    /// </summary>
    void GoBack();

    /// <summary>
    /// Check if can go back.
    /// </summary>
    bool CanGoBack { get; }

    /// <summary>
    /// Get navigation parameter.
    /// </summary>
    T? GetParameter<T>() where T : class;
}
