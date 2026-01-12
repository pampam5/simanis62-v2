using System.IO;
using Serilog;
using Serilog.Events;
using Simanis62.Core.Configuration;

namespace Simanis62.Core.Logging;

/// <summary>
/// Service untuk setup Serilog logging dengan GlitchTip/Sentry integration.
/// </summary>
public static class LoggingService
{
    public static void Initialize(AppSettings settings)
    {
        var logLevel = settings.LogLevel.ToLower() switch
        {
            "debug" => LogEventLevel.Debug,
            "information" => LogEventLevel.Information,
            "warning" => LogEventLevel.Warning,
            "error" => LogEventLevel.Error,
            _ => LogEventLevel.Information
        };

        // Ensure log directory exists
        var logDirectory = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "Simanis62",
            settings.LogDirectory);

        Directory.CreateDirectory(logDirectory);

        var logPath = Path.Combine(logDirectory, "simanis62-wpf-.log");

        var logConfig = new LoggerConfiguration()
            .MinimumLevel.Is(logLevel)
            .Enrich.WithProperty("Application", "SIMANIS62.WPF")
            .Enrich.WithProperty("Environment", settings.Environment)
            .WriteTo.Console(
                outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}")
            .WriteTo.File(
                logPath,
                rollingInterval: RollingInterval.Day,
                retainedFileCountLimit: 7,
                outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj}{NewLine}{Exception}");

        // Add GlitchTip/Sentry if DSN is configured
        if (!string.IsNullOrEmpty(settings.GlitchTipDsn))
        {
            logConfig.WriteTo.Sentry(o =>
            {
                o.Dsn = settings.GlitchTipDsn;
                o.MinimumEventLevel = LogEventLevel.Error;
                o.MinimumBreadcrumbLevel = LogEventLevel.Information;
                o.InitializeSdk = true;
            });
        }

        Log.Logger = logConfig.CreateLogger();
    }
}
