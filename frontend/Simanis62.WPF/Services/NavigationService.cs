using Simanis62.Services.Interfaces;

namespace Simanis62.Services;

/// <summary>
/// Implementation of navigation service.
/// </summary>
public class NavigationService : INavigationService
{
    private readonly Stack<(string ViewName, object? Parameter)> _navigationStack = new();
    private object? _currentParameter;

    public string CurrentView { get; private set; } = "Login";
    public bool CanGoBack => _navigationStack.Count > 1;

    public event Action<string>? NavigationChanged;

    public void NavigateTo(string viewName, object? parameter = null)
    {
        _navigationStack.Push((viewName, parameter));
        CurrentView = viewName;
        _currentParameter = parameter;
        NavigationChanged?.Invoke(viewName);
    }

    public void GoBack()
    {
        if (_navigationStack.Count > 1)
        {
            _navigationStack.Pop();
            var (viewName, parameter) = _navigationStack.Peek();
            CurrentView = viewName;
            _currentParameter = parameter;
            NavigationChanged?.Invoke(viewName);
        }
    }

    public T? GetParameter<T>() where T : class
    {
        return _currentParameter as T;
    }
}
