using Simanis62.Models;

namespace Simanis62.Services.Interfaces;

/// <summary>
/// Service interface untuk First-Run Setup Wizard.
/// </summary>
public interface ISetupService
{
    /// <summary>
    /// Check apakah aplikasi memerlukan setup awal.
    /// </summary>
    /// <returns>True jika setup diperlukan (no users exist)</returns>
    Task<bool> CheckSetupStatusAsync();

    /// <summary>
    /// Buat akun administrator pertama.
    /// </summary>
    /// <param name="username">Username untuk admin</param>
    /// <param name="password">Password untuk admin</param>
    /// <param name="namaLengkap">Nama lengkap admin</param>
    /// <returns>Response dengan data admin yang dibuat</returns>
    Task<ApiResponse<CreateAdminResponse>> CreateFirstAdminAsync(
        string username,
        string password,
        string namaLengkap);
}

/// <summary>
/// Response model untuk setup status.
/// </summary>
public class SetupStatusResponse
{
    public bool NeedsSetup { get; set; }
    public string Message { get; set; } = string.Empty;
}

/// <summary>
/// Request model untuk create admin.
/// </summary>
public class CreateAdminRequest
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public string NamaLengkap { get; set; } = string.Empty;
}

/// <summary>
/// Response model untuk created admin.
/// </summary>
public class CreateAdminResponse
{
    public string Id { get; set; } = string.Empty;
    public string Username { get; set; } = string.Empty;
    public string NamaLengkap { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public bool DapatEkspor { get; set; }
}
