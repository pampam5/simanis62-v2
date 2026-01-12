using System.Windows;
using MaterialDesignThemes.Wpf;
using Simanis62.Services.Interfaces;

namespace Simanis62.Services;

/// <summary>
/// Implementation of dialog service using MaterialDesign.
/// </summary>
public class DialogService : IDialogService
{
    private ISnackbarMessageQueue? _snackbarQueue;

    public void SetSnackbarQueue(ISnackbarMessageQueue queue)
    {
        _snackbarQueue = queue;
    }

    public Task ShowInfoAsync(string title, string message)
    {
        MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Information);
        return Task.CompletedTask;
    }

    public Task ShowErrorAsync(string title, string message)
    {
        MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Error);
        return Task.CompletedTask;
    }

    public Task ShowWarningAsync(string title, string message)
    {
        MessageBox.Show(message, title, MessageBoxButton.OK, MessageBoxImage.Warning);
        return Task.CompletedTask;
    }

    public Task<bool> ShowConfirmAsync(string title, string message)
    {
        var result = MessageBox.Show(message, title, MessageBoxButton.YesNo, MessageBoxImage.Question);
        return Task.FromResult(result == MessageBoxResult.Yes);
    }

    public Task<string?> ShowInputAsync(string title, string message, string defaultValue = "")
    {
        // Simple input dialog - can be enhanced with MaterialDesign dialog
        var result = Microsoft.VisualBasic.Interaction.InputBox(message, title, defaultValue);
        return Task.FromResult(string.IsNullOrEmpty(result) ? null : result);
    }

    public void ShowSnackbar(string message, int durationMs = 3000)
    {
        _snackbarQueue?.Enqueue(message, null, null, null, false, true, TimeSpan.FromMilliseconds(durationMs));
    }
}
