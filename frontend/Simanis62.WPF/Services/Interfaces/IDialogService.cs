namespace Simanis62.Services.Interfaces;

/// <summary>
/// Service untuk menampilkan dialog.
/// </summary>
public interface IDialogService
{
    /// <summary>
    /// Show information message.
    /// </summary>
    Task ShowInfoAsync(string title, string message);

    /// <summary>
    /// Show error message.
    /// </summary>
    Task ShowErrorAsync(string title, string message);

    /// <summary>
    /// Show warning message.
    /// </summary>
    Task ShowWarningAsync(string title, string message);

    /// <summary>
    /// Show confirmation dialog.
    /// </summary>
    Task<bool> ShowConfirmAsync(string title, string message);

    /// <summary>
    /// Show input dialog.
    /// </summary>
    Task<string?> ShowInputAsync(string title, string message, string defaultValue = "");

    /// <summary>
    /// Show snackbar notification.
    /// </summary>
    void ShowSnackbar(string message, int durationMs = 3000);
}
