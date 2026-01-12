using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk halaman login.
/// </summary>
public partial class LoginViewModel : ViewModelBase
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(LoginCommand))]
    private string _username = string.Empty;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(LoginCommand))]
    private string _password = string.Empty;

    [ObservableProperty]
    private bool _rememberMe;

    public LoginViewModel(
        IApiService apiService,
        INavigationService navigationService,
        IDialogService dialogService,
        ISessionService sessionService)
        : base(navigationService, dialogService, sessionService)
    {
        _apiService = apiService;
    }

    private bool CanLogin => !string.IsNullOrWhiteSpace(Username) && !string.IsNullOrWhiteSpace(Password) && !IsBusy;

    [RelayCommand(CanExecute = nameof(CanLogin))]
    private async Task LoginAsync()
    {
        await ExecuteAsync(async () =>
        {
            Log.Information("Login attempt for user: {Username}", Username);

            var response = await _apiService.LoginAsync(new LoginRequest
            {
                Username = Username,
                Password = Password
            });

            if (response.Success && response.Data != null)
            {
                SessionService.SetUser(response.Data.User);
                Log.Information("Login successful for user: {Username}", Username);

                DialogService.ShowSnackbar($"Selamat datang, {response.Data.User.NamaLengkap}!");
                NavigationService.NavigateTo("Dashboard");
            }
            else
            {
                SetError(response.Message ?? "Login gagal");
            }
        });
    }

    partial void OnUsernameChanged(string value)
    {
        ClearError();
    }

    partial void OnPasswordChanged(string value)
    {
        ClearError();
    }
}
