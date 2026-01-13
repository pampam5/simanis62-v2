using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Serilog;
using Simanis62.Core.Configuration;
using Simanis62.Core.Logging;
using Simanis62.Services;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels;
using Simanis62.Views;

namespace Simanis62;

/// <summary>
/// Application entry point dengan Dependency Injection.
/// </summary>
public partial class App : Application
{
    private readonly IServiceProvider _serviceProvider;
    private readonly AppSettings _appSettings;

    public static IServiceProvider Services { get; private set; } = null!;

    public App()
    {
        var services = new ServiceCollection();
        _appSettings = ConfigureServices(services);
        _serviceProvider = services.BuildServiceProvider();
        Services = _serviceProvider;
    }

    private AppSettings ConfigureServices(IServiceCollection services)
    {
        // Configuration
        var configuration = new ConfigurationBuilder()
            .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .Build();

        services.AddSingleton<IConfiguration>(configuration);

        var appSettings = configuration.GetSection("AppSettings").Get<AppSettings>() ?? new AppSettings();
        services.AddSingleton(appSettings);

        // Logging
        LoggingService.Initialize(appSettings);
        services.AddSingleton(Log.Logger);

        // Services
        services.AddSingleton<INavigationService, NavigationService>();
        services.AddSingleton<IDialogService, DialogService>();
        
        // API Service dengan Polly resilience policies
        services.AddHttpClient<IApiService, ApiService>(client =>
        {
            client.BaseAddress = new Uri(appSettings.ApiBaseUrl);
            client.Timeout = TimeSpan.FromSeconds(30);
        })
        .AddPolicyHandler(ResiliencePolicies.GetRetryPolicy())
        .AddPolicyHandler(ResiliencePolicies.GetCircuitBreakerPolicy());
        
        services.AddSingleton<ISessionService, SessionService>();

        // Setup Service dengan Polly resilience policies
        services.AddHttpClient<ISetupService, SetupService>(client =>
        {
            client.BaseAddress = new Uri(appSettings.ApiBaseUrl);
            client.Timeout = TimeSpan.FromSeconds(30);
        })
        .AddPolicyHandler(ResiliencePolicies.GetRetryPolicy());

        // ViewModels
        services.AddTransient<LoginViewModel>();
        services.AddTransient<DashboardViewModel>();
        services.AddTransient<AssetListViewModel>();
        services.AddTransient<AssetFormViewModel>();
        services.AddTransient<KibReportViewModel>();
        services.AddTransient<MutationViewModel>();
        services.AddTransient<MainViewModel>();
        services.AddTransient<SetupWizardViewModel>();

        // Views
        services.AddTransient<LoginView>();
        services.AddTransient<DashboardView>();
        services.AddTransient<AssetListView>();
        services.AddTransient<AssetFormView>();
        services.AddTransient<KibReportView>();
        services.AddTransient<MutationView>();
        services.AddTransient<SetupWizardView>();
        services.AddSingleton<MainWindow>();

        return appSettings;
    }

    protected override async void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        Log.Information("SIMANIS62 starting...");

        // Setup global exception handlers
        SetupExceptionHandling();

        // Check if first-run setup is needed
        var needsSetup = await CheckSetupStatusAsync();

        // Show main window
        var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
        mainWindow.Show();

        // Navigate to appropriate view
        var navigationService = _serviceProvider.GetRequiredService<INavigationService>();
        if (needsSetup)
        {
            Log.Information("First-run setup required, showing Setup Wizard");
            navigationService.NavigateTo("SetupWizard");
        }
        else
        {
            Log.Information("Setup complete, showing Login");
            navigationService.NavigateTo("Login");
        }
    }

    /// <summary>
    /// Check apakah aplikasi memerlukan first-run setup.
    /// Jika backend tidak tersedia, return false (lanjut ke Login, error akan ditampilkan di sana).
    /// </summary>
    private async Task<bool> CheckSetupStatusAsync()
    {
        try
        {
            Log.Information("Checking setup status from backend...");

            var setupService = _serviceProvider.GetRequiredService<ISetupService>();
            var needsSetup = await setupService.CheckSetupStatusAsync();

            Log.Information("Setup status check complete: needs_setup={NeedsSetup}", needsSetup);
            return needsSetup;
        }
        catch (Exception ex)
        {
            // Jika backend tidak tersedia, log warning dan lanjut ke Login
            // User akan melihat error di LoginView saat mencoba login
            Log.Warning(ex, "Failed to check setup status - backend may not be running");

            // Show warning dialog
            MessageBox.Show(
                "Tidak dapat terhubung ke server backend.\n\n" +
                "Pastikan Simanis62.API sudah berjalan sebelum menggunakan aplikasi.\n\n" +
                "Aplikasi akan melanjutkan ke halaman Login.",
                "Peringatan",
                MessageBoxButton.OK,
                MessageBoxImage.Warning);

            return false;
        }
    }

    private void SetupExceptionHandling()
    {
        // Domain-level unhandled exceptions (fatal errors)
        AppDomain.CurrentDomain.UnhandledException += (s, e) =>
        {
            var exception = e.ExceptionObject as Exception;
            Log.Fatal(exception, "Unhandled domain exception - application may terminate");
            
            // Show error to user before crash
            MessageBox.Show(
                $"Terjadi kesalahan fatal:\n\n{exception?.Message}\n\nAplikasi akan ditutup.",
                "Error Fatal",
                MessageBoxButton.OK,
                MessageBoxImage.Error);
        };

        // UI thread exceptions
        DispatcherUnhandledException += (s, e) =>
        {
            Log.Error(e.Exception, "Unhandled dispatcher exception: {Message}", e.Exception.Message);
            
            // Handle specific exception types
            var message = e.Exception switch
            {
                Simanis62.Core.Exceptions.SessionExpiredException => 
                    "Session Anda telah berakhir. Silakan login kembali.",
                Simanis62.Core.Exceptions.ApiConnectionException => 
                    "Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.",
                Simanis62.Core.Exceptions.AuthorizationException => 
                    "Anda tidak memiliki izin untuk melakukan aksi ini.",
                _ => $"Terjadi kesalahan: {e.Exception.Message}"
            };

            MessageBox.Show(message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            
            // Handle session expired - navigate to login
            if (e.Exception is Simanis62.Core.Exceptions.SessionExpiredException)
            {
                try
                {
                    var sessionService = _serviceProvider.GetService<ISessionService>();
                    var navigationService = _serviceProvider.GetService<INavigationService>();
                    sessionService?.ClearSession();
                    navigationService?.NavigateTo("Login");
                }
                catch (Exception navEx)
                {
                    Log.Error(navEx, "Failed to navigate to login after session expired");
                }
            }
            
            e.Handled = true;
        };

        // Background task exceptions (async/await without proper handling)
        TaskScheduler.UnobservedTaskException += (s, e) =>
        {
            Log.Error(e.Exception, "Unobserved task exception: {Message}", e.Exception.Message);
            
            // Check if it's a session expired exception
            var sessionExpired = e.Exception.InnerExceptions
                .Any(ex => ex is Simanis62.Core.Exceptions.SessionExpiredException);
            
            if (sessionExpired)
            {
                // Dispatch to UI thread to show message and navigate
                Current.Dispatcher.BeginInvoke(() =>
                {
                    MessageBox.Show(
                        "Session Anda telah berakhir. Silakan login kembali.",
                        "Session Expired",
                        MessageBoxButton.OK,
                        MessageBoxImage.Warning);
                    
                    try
                    {
                        var sessionService = _serviceProvider.GetService<ISessionService>();
                        var navigationService = _serviceProvider.GetService<INavigationService>();
                        sessionService?.ClearSession();
                        navigationService?.NavigateTo("Login");
                    }
                    catch { }
                });
            }
            
            e.SetObserved();
        };
    }

    protected override void OnExit(ExitEventArgs e)
    {
        Log.Information("SIMANIS62 shutting down...");
        Log.CloseAndFlush();
        base.OnExit(e);
    }
}
