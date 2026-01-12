namespace Simanis62.Core.Configuration;

/// <summary>
/// Application settings loaded from appsettings.json.
/// </summary>
public class AppSettings
{
    public string ApiBaseUrl { get; set; } = "http://127.0.0.1:8000";
    public int SessionTimeoutMinutes { get; set; } = 120;
    public string LogLevel { get; set; } = "Information";
    public string LogDirectory { get; set; } = "logs";
    public string GlitchTipDsn { get; set; } = string.Empty;
    public string Environment { get; set; } = "Development";
}
