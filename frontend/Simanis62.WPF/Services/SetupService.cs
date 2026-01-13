using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;

namespace Simanis62.Services;

/// <summary>
/// Service implementation untuk First-Run Setup Wizard.
/// </summary>
public class SetupService : ISetupService
{
    private readonly HttpClient _httpClient;
    private readonly JsonSerializerOptions _jsonOptions;

    public SetupService(HttpClient httpClient)
    {
        _httpClient = httpClient;
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            PropertyNameCaseInsensitive = true
        };
    }

    /// <inheritdoc/>
    public async Task<bool> CheckSetupStatusAsync()
    {
        try
        {
            Log.Information("Checking setup status...");

            var response = await _httpClient.GetAsync("/api/v1/setup/status");
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadFromJsonAsync<ApiResponse<SetupStatusResponse>>(_jsonOptions);

            if (result?.Success == true && result.Data != null)
            {
                Log.Information("Setup status: needs_setup={NeedsSetup}", result.Data.NeedsSetup);
                return result.Data.NeedsSetup;
            }

            Log.Warning("Failed to parse setup status response");
            return false;
        }
        catch (HttpRequestException ex)
        {
            Log.Error(ex, "Failed to check setup status - API not available");
            // If API is not available, assume setup is not needed (will show error on login)
            return false;
        }
        catch (Exception ex)
        {
            Log.Error(ex, "Unexpected error checking setup status");
            return false;
        }
    }

    /// <inheritdoc/>
    public async Task<ApiResponse<CreateAdminResponse>> CreateFirstAdminAsync(
        string username,
        string password,
        string namaLengkap)
    {
        try
        {
            Log.Information("Creating first admin: {Username}", username);

            var request = new CreateAdminRequest
            {
                Username = username,
                Password = password,
                NamaLengkap = namaLengkap
            };

            var response = await _httpClient.PostAsJsonAsync("/api/v1/setup/admin", request, _jsonOptions);

            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadFromJsonAsync<ApiResponse<CreateAdminResponse>>(_jsonOptions);
                if (result != null)
                {
                    Log.Information("First admin created successfully: {Username}", username);
                    return result;
                }
            }

            // Handle error response
            var errorContent = await response.Content.ReadAsStringAsync();
            Log.Warning("Failed to create admin: {StatusCode} - {Content}", response.StatusCode, errorContent);

            return new ApiResponse<CreateAdminResponse>
            {
                Success = false,
                Message = ParseErrorMessage(errorContent) ?? "Gagal membuat administrator"
            };
        }
        catch (HttpRequestException ex)
        {
            Log.Error(ex, "Failed to create admin - API not available");
            return new ApiResponse<CreateAdminResponse>
            {
                Success = false,
                Message = "Tidak dapat terhubung ke server. Pastikan backend sudah berjalan."
            };
        }
        catch (Exception ex)
        {
            Log.Error(ex, "Unexpected error creating admin");
            return new ApiResponse<CreateAdminResponse>
            {
                Success = false,
                Message = "Terjadi kesalahan. Silakan coba lagi."
            };
        }
    }

    private static string? ParseErrorMessage(string errorContent)
    {
        try
        {
            using var doc = JsonDocument.Parse(errorContent);
            if (doc.RootElement.TryGetProperty("detail", out var detail))
            {
                if (detail.ValueKind == JsonValueKind.Object &&
                    detail.TryGetProperty("message", out var message))
                {
                    return message.GetString();
                }
                if (detail.ValueKind == JsonValueKind.String)
                {
                    return detail.GetString();
                }
            }
            if (doc.RootElement.TryGetProperty("message", out var msg))
            {
                return msg.GetString();
            }
        }
        catch
        {
            // Ignore parsing errors
        }
        return null;
    }
}
