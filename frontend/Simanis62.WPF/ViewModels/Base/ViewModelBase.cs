using System.Net.Http;
using CommunityToolkit.Mvvm.ComponentModel;
using Serilog;
using Simanis62.Core.Exceptions;
using Simanis62.Services.Interfaces;

namespace Simanis62.ViewModels.Base;

/// <summary>
/// Base class untuk semua ViewModels.
/// </summary>
public abstract partial class ViewModelBase : ObservableObject
{
    protected readonly INavigationService NavigationService;
    protected readonly IDialogService DialogService;
    protected readonly ISessionService SessionService;

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(IsNotBusy))]
    private bool _isBusy;

    [ObservableProperty]
    private string? _errorMessage;

    [ObservableProperty]
    private bool _hasError;

    public bool IsNotBusy => !IsBusy;

    protected ViewModelBase(
        INavigationService navigationService,
        IDialogService dialogService,
        ISessionService sessionService)
    {
        NavigationService = navigationService;
        DialogService = dialogService;
        SessionService = sessionService;
    }

    /// <summary>
    /// Execute async operation with error handling.
    /// </summary>
    protected async Task ExecuteAsync(Func<Task> operation, string? loadingMessage = null)
    {
        if (IsBusy) return;

        try
        {
            IsBusy = true;
            ClearError();
            await operation();
        }
        catch (SessionExpiredException)
        {
            await HandleSessionExpired();
        }
        catch (AuthorizationException ex)
        {
            SetError(ex.Message);
            await DialogService.ShowErrorAsync("Akses Ditolak", ex.Message);
        }
        catch (ApiConnectionException ex)
        {
            SetError(ex.Message);
            Log.Warning(ex, "API connection error");
            await DialogService.ShowErrorAsync("Koneksi Gagal", 
                "Tidak dapat terhubung ke server.\n\nPastikan backend sudah berjalan dan coba lagi.");
        }
        catch (SimanisException ex)
        {
            SetError(ex.Message);
            Log.Warning(ex, "Business error: {ErrorCode}", ex.ErrorCode);
        }
        catch (HttpRequestException ex)
        {
            SetError("Tidak dapat terhubung ke server");
            Log.Warning(ex, "HTTP request error");
            await DialogService.ShowErrorAsync("Koneksi Gagal", 
                "Tidak dapat terhubung ke server.\n\nPastikan backend sudah berjalan dan coba lagi.");
        }
        catch (TaskCanceledException ex) when (ex.InnerException is TimeoutException)
        {
            SetError("Request timeout");
            Log.Warning(ex, "Request timeout");
            await DialogService.ShowErrorAsync("Timeout", 
                "Request memakan waktu terlalu lama. Silakan coba lagi.");
        }
        catch (Exception ex)
        {
            SetError("Terjadi kesalahan yang tidak terduga");
            Log.Error(ex, "Unexpected error in ViewModel");
            await DialogService.ShowErrorAsync("Error", "Terjadi kesalahan yang tidak terduga. Silakan coba lagi.");
        }
        finally
        {
            IsBusy = false;
        }
    }

    /// <summary>
    /// Execute async operation with result.
    /// </summary>
    protected async Task<T?> ExecuteAsync<T>(Func<Task<T>> operation, string? loadingMessage = null)
    {
        if (IsBusy) return default;

        try
        {
            IsBusy = true;
            ClearError();
            return await operation();
        }
        catch (SessionExpiredException)
        {
            await HandleSessionExpired();
            return default;
        }
        catch (AuthorizationException ex)
        {
            SetError(ex.Message);
            await DialogService.ShowErrorAsync("Akses Ditolak", ex.Message);
            return default;
        }
        catch (ApiConnectionException ex)
        {
            SetError(ex.Message);
            Log.Warning(ex, "API connection error");
            await DialogService.ShowErrorAsync("Koneksi Gagal", 
                "Tidak dapat terhubung ke server.\n\nPastikan backend sudah berjalan dan coba lagi.");
            return default;
        }
        catch (SimanisException ex)
        {
            SetError(ex.Message);
            Log.Warning(ex, "Business error: {ErrorCode}", ex.ErrorCode);
            return default;
        }
        catch (HttpRequestException ex)
        {
            SetError("Tidak dapat terhubung ke server");
            Log.Warning(ex, "HTTP request error");
            await DialogService.ShowErrorAsync("Koneksi Gagal", 
                "Tidak dapat terhubung ke server.\n\nPastikan backend sudah berjalan dan coba lagi.");
            return default;
        }
        catch (TaskCanceledException ex) when (ex.InnerException is TimeoutException)
        {
            SetError("Request timeout");
            Log.Warning(ex, "Request timeout");
            await DialogService.ShowErrorAsync("Timeout", 
                "Request memakan waktu terlalu lama. Silakan coba lagi.");
            return default;
        }
        catch (Exception ex)
        {
            SetError("Terjadi kesalahan yang tidak terduga");
            Log.Error(ex, "Unexpected error in ViewModel");
            await DialogService.ShowErrorAsync("Error", "Terjadi kesalahan yang tidak terduga. Silakan coba lagi.");
            return default;
        }
        finally
        {
            IsBusy = false;
        }
    }

    protected void SetError(string message)
    {
        ErrorMessage = message;
        HasError = true;
    }

    protected void ClearError()
    {
        ErrorMessage = null;
        HasError = false;
    }

    private async Task HandleSessionExpired()
    {
        SessionService.ClearSession();
        await DialogService.ShowWarningAsync("Session Berakhir", "Session Anda telah berakhir. Silakan login kembali.");
        NavigationService.NavigateTo("Login");
    }

    /// <summary>
    /// Called when view is loaded.
    /// </summary>
    public virtual Task OnLoadedAsync() => Task.CompletedTask;

    /// <summary>
    /// Called when view is unloaded.
    /// </summary>
    public virtual Task OnUnloadedAsync() => Task.CompletedTask;
}
