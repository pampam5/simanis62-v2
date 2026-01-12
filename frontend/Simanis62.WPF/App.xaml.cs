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

    public static IServiceProvider Services { get; private set; } = null!;

    public App()
    {
        var services = new ServiceCollection();
        ConfigureServices(services);
        _serviceProvider = services.BuildServiceProvider();
        Services = _serviceProvider;
    }

    private void ConfigureServices(IServiceCollection services)
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
        services.AddHttpClient<IApiService, ApiService>(client =>
        {
            client.BaseAddress = new Uri(appSettings.ApiBaseUrl);
            client.Timeout = TimeSpan.FromSeconds(30);
        });
        services.AddSingleton<ISessionService, SessionService>();

        // ViewModels
        services.AddTransient<LoginViewModel>();
        services.AddTransient<DashboardViewModel>();
        services.AddTransient<AssetListViewModel>();
        services.AddTransient<AssetFormViewModel>();
        services.AddTransient<KibReportViewModel>();
        services.AddTransient<MutationViewModel>();
        services.AddTransient<MainViewModel>();

        // Views
        services.AddTransient<LoginView>();
        services.AddTransient<DashboardView>();
        services.AddTransient<AssetListView>();
        services.AddTransient<AssetFormView>();
        services.AddTransient<KibReportView>();
        services.AddTransient<MutationView>();
        services.AddSingleton<MainWindow>();
    }

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        Log.Information("SIMANIS62 starting...");

        // Setup global exception handlers
        SetupExceptionHandling();

        // Show main window
        var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
        mainWindow.Show();
    }

    private void SetupExceptionHandling()
    {
        AppDomain.CurrentDomain.UnhandledException += (s, e) =>
        {
            Log.Fatal(e.ExceptionObject as Exception, "Unhandled domain exception");
        };

        DispatcherUnhandledException += (s, e) =>
        {
            Log.Error(e.Exception, "Unhandled dispatcher exception");
            MessageBox.Show(
                "Terjadi kesalahan yang tidak terduga. Silakan restart aplikasi.",
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.Error);
            e.Handled = true;
        };

        TaskScheduler.UnobservedTaskException += (s, e) =>
        {
            Log.Error(e.Exception, "Unobserved task exception");
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
