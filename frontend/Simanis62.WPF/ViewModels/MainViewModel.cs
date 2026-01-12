using System.Windows.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk MainWindow (shell).
/// </summary>
public partial class MainViewModel : ViewModelBase
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private string _currentViewName = "Login";

    [ObservableProperty]
    private bool _isLoggedIn;

    [ObservableProperty]
    private string _userName = string.Empty;

    [ObservableProperty]
    private string _userRole = string.Empty;

    [ObservableProperty]
    private bool _isSidebarExpanded = true;

    [ObservableProperty]
    private UserControl? _currentView;

    public bool IsAdmin => SessionService.IsAdmin;
    public bool CanExport => SessionService.CanExport;
    public int SidebarWidth => IsSidebarExpanded ? 250 : 60;

    public MainViewModel(
        IApiService apiService,
        INavigationService navigationService,
        IDialogService dialogService,
        ISessionService sessionService)
        : base(navigationService, dialogService, sessionService)
    {
        _apiService = apiService;

        // Subscribe to navigation changes
        NavigationService.NavigationChanged += OnNavigationChanged;
        SessionService.SessionChanged += OnSessionChanged;
    }

    private void OnNavigationChanged(string viewName)
    {
        CurrentViewName = viewName;
    }

    private void OnSessionChanged()
    {
        IsLoggedIn = SessionService.IsLoggedIn;
        if (SessionService.CurrentUser != null)
        {
            UserName = SessionService.CurrentUser.NamaLengkap;
            UserRole = SessionService.CurrentUser.Role;
        }
        else
        {
            UserName = string.Empty;
            UserRole = string.Empty;
        }

        OnPropertyChanged(nameof(IsAdmin));
        OnPropertyChanged(nameof(CanExport));
    }

    [RelayCommand]
    private void NavigateTo(string viewName)
    {
        NavigationService.NavigateTo(viewName);
    }

    [RelayCommand]
    private void GoBack()
    {
        if (NavigationService.CanGoBack)
        {
            NavigationService.GoBack();
        }
    }

    [RelayCommand]
    private void ToggleSidebar()
    {
        IsSidebarExpanded = !IsSidebarExpanded;
    }

    [RelayCommand]
    private async Task LogoutAsync()
    {
        var confirm = await DialogService.ShowConfirmAsync(
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin keluar?");

        if (!confirm) return;

        await ExecuteAsync(async () =>
        {
            Log.Information("User logging out: {Username}", SessionService.CurrentUser?.Username);

            try
            {
                await _apiService.LogoutAsync();
            }
            catch
            {
                // Ignore logout API errors
            }

            SessionService.ClearSession();
            NavigationService.NavigateTo("Login");
            DialogService.ShowSnackbar("Anda telah keluar dari sistem");
        });
    }
}
