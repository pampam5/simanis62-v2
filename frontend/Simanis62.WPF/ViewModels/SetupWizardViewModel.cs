using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk First-Run Setup Wizard.
/// 3-step wizard: Welcome → Create Admin → Success
/// </summary>
public partial class SetupWizardViewModel : ViewModelBase
{
    private readonly ISetupService _setupService;

    [ObservableProperty]
    private int _currentStep = 1;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(CreateAdminCommand))]
    private string _username = string.Empty;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(CreateAdminCommand))]
    private string _password = string.Empty;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(CreateAdminCommand))]
    private string _confirmPassword = string.Empty;

    [ObservableProperty]
    [NotifyCanExecuteChangedFor(nameof(CreateAdminCommand))]
    private string _namaLengkap = string.Empty;

    [ObservableProperty]
    private CreateAdminResponse? _createdAdmin;

    // Validation error messages
    [ObservableProperty]
    private string _usernameError = string.Empty;

    [ObservableProperty]
    private string _passwordError = string.Empty;

    [ObservableProperty]
    private string _confirmPasswordError = string.Empty;

    [ObservableProperty]
    private string _namaLengkapError = string.Empty;

    public SetupWizardViewModel(
        ISetupService setupService,
        INavigationService navigationService,
        IDialogService dialogService,
        ISessionService sessionService)
        : base(navigationService, dialogService, sessionService)
    {
        _setupService = setupService;
    }

    public bool IsStep1 => CurrentStep == 1;
    public bool IsStep2 => CurrentStep == 2;
    public bool IsStep3 => CurrentStep == 3;

    public bool CanGoBack => CurrentStep == 2 && !IsBusy;

    private bool CanCreateAdmin =>
        !string.IsNullOrWhiteSpace(Username) &&
        Username.Length >= 5 &&
        !string.IsNullOrWhiteSpace(Password) &&
        Password.Length >= 8 &&
        Password == ConfirmPassword &&
        !string.IsNullOrWhiteSpace(NamaLengkap) &&
        NamaLengkap.Length >= 3 &&
        !IsBusy;

    [RelayCommand]
    private void NextStep()
    {
        if (CurrentStep < 3)
        {
            CurrentStep++;
            NotifyStepChanged();
        }
    }

    [RelayCommand(CanExecute = nameof(CanGoBack))]
    private void PreviousStep()
    {
        if (CurrentStep > 1)
        {
            CurrentStep--;
            NotifyStepChanged();
        }
    }

    [RelayCommand(CanExecute = nameof(CanCreateAdmin))]
    private async Task CreateAdminAsync()
    {
        // Validate before submit
        if (!ValidateForm())
        {
            return;
        }

        await ExecuteAsync(async () =>
        {
            Log.Information("Creating first admin: {Username}", Username);

            var response = await _setupService.CreateFirstAdminAsync(
                Username,
                Password,
                NamaLengkap);

            if (response.Success && response.Data != null)
            {
                CreatedAdmin = response.Data;
                CurrentStep = 3;
                NotifyStepChanged();
                Log.Information("First admin created successfully");
            }
            else
            {
                SetError(response.Message ?? "Gagal membuat administrator");
            }
        });
    }

    [RelayCommand]
    private void StartApplication()
    {
        Log.Information("Setup complete, navigating to login");
        NavigationService.NavigateTo("Login");
    }

    private bool ValidateForm()
    {
        var isValid = true;

        // Validate username
        if (string.IsNullOrWhiteSpace(Username))
        {
            UsernameError = "Username harus diisi";
            isValid = false;
        }
        else if (Username.Length < 5)
        {
            UsernameError = "Username minimal 5 karakter";
            isValid = false;
        }
        else if (!IsValidUsername(Username))
        {
            UsernameError = "Username hanya boleh huruf, angka, dan underscore";
            isValid = false;
        }
        else
        {
            UsernameError = string.Empty;
        }

        // Validate password
        if (string.IsNullOrWhiteSpace(Password))
        {
            PasswordError = "Password harus diisi";
            isValid = false;
        }
        else if (Password.Length < 8)
        {
            PasswordError = "Password minimal 8 karakter";
            isValid = false;
        }
        else
        {
            PasswordError = string.Empty;
        }

        // Validate confirm password
        if (Password != ConfirmPassword)
        {
            ConfirmPasswordError = "Password tidak sama";
            isValid = false;
        }
        else
        {
            ConfirmPasswordError = string.Empty;
        }

        // Validate nama lengkap
        if (string.IsNullOrWhiteSpace(NamaLengkap))
        {
            NamaLengkapError = "Nama lengkap harus diisi";
            isValid = false;
        }
        else if (NamaLengkap.Length < 3)
        {
            NamaLengkapError = "Nama lengkap minimal 3 karakter";
            isValid = false;
        }
        else
        {
            NamaLengkapError = string.Empty;
        }

        return isValid;
    }

    private static bool IsValidUsername(string username)
    {
        return username.Replace("_", "").All(char.IsLetterOrDigit);
    }

    private void NotifyStepChanged()
    {
        OnPropertyChanged(nameof(IsStep1));
        OnPropertyChanged(nameof(IsStep2));
        OnPropertyChanged(nameof(IsStep3));
        OnPropertyChanged(nameof(CanGoBack));
        PreviousStepCommand.NotifyCanExecuteChanged();
    }

    partial void OnUsernameChanged(string value)
    {
        ClearError();
        UsernameError = string.Empty;
    }

    partial void OnPasswordChanged(string value)
    {
        ClearError();
        PasswordError = string.Empty;
        // Re-validate confirm password
        if (!string.IsNullOrEmpty(ConfirmPassword) && value != ConfirmPassword)
        {
            ConfirmPasswordError = "Password tidak sama";
        }
        else
        {
            ConfirmPasswordError = string.Empty;
        }
    }

    partial void OnConfirmPasswordChanged(string value)
    {
        ClearError();
        if (value != Password)
        {
            ConfirmPasswordError = "Password tidak sama";
        }
        else
        {
            ConfirmPasswordError = string.Empty;
        }
    }

    partial void OnNamaLengkapChanged(string value)
    {
        ClearError();
        NamaLengkapError = string.Empty;
    }
}
