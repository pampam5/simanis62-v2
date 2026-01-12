using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using Refit;
using Serilog;
using Simanis62.Core.Exceptions;
using Simanis62.Models;
using Simanis62.Services.Interfaces;

namespace Simanis62.Services;

/// <summary>
/// Implementation of IApiService with error handling.
/// </summary>
public class ApiService : IApiService
{
    private readonly HttpClient _httpClient;
    private readonly IApiService _refitClient;
    private readonly JsonSerializerOptions _jsonOptions;

    public ApiService(HttpClient httpClient)
    {
        _httpClient = httpClient;
        _httpClient.DefaultRequestHeaders.Add("Accept", "application/json");

        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            PropertyNameCaseInsensitive = true
        };

        _refitClient = RestService.For<IApiService>(_httpClient, new RefitSettings
        {
            ContentSerializer = new SystemTextJsonContentSerializer(_jsonOptions)
        });
    }

    // === Auth ===
    public async Task<Models.ApiResponse<LoginResponse>> LoginAsync(LoginRequest request)
    {
        try
        {
            return await _refitClient.LoginAsync(request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<object>> LogoutAsync()
    {
        try
        {
            return await _refitClient.LogoutAsync();
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<User>> GetCurrentUserAsync()
    {
        try
        {
            return await _refitClient.GetCurrentUserAsync();
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    // === Assets ===
    public async Task<PaginatedResponse<Asset>> GetAssetsAsync(
        string? keyword = null, string? kategori_kib = null, string? status = null,
        Guid? ruangan_id = null, int page = 1, int page_size = 100)
    {
        try
        {
            return await _refitClient.GetAssetsAsync(keyword, kategori_kib, status, ruangan_id, page, page_size);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Asset>> GetAssetByIdAsync(Guid id)
    {
        try
        {
            return await _refitClient.GetAssetByIdAsync(id);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Asset>> CreateAssetAsync(AssetRequest request)
    {
        try
        {
            return await _refitClient.CreateAssetAsync(request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Asset>> UpdateAssetAsync(Guid id, AssetRequest request)
    {
        try
        {
            return await _refitClient.UpdateAssetAsync(id, request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<object>> DeleteAssetAsync(Guid id, AssetDeleteRequest request)
    {
        try
        {
            return await _refitClient.DeleteAssetAsync(id, request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    // === KIB Reports ===
    public async Task<Models.ApiResponse<KibReportResponse>> GetKibReportAsync(string kategori)
    {
        try
        {
            return await _refitClient.GetKibReportAsync(kategori);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<HttpResponseMessage> ExportKibAsync(string kategori)
    {
        try
        {
            return await _refitClient.ExportKibAsync(kategori);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    // === Mutations ===
    public async Task<PaginatedResponse<Mutation>> GetMutationsAsync(string? status = null, int page = 1, int page_size = 100)
    {
        try
        {
            return await _refitClient.GetMutationsAsync(status, page, page_size);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Mutation>> GetMutationByIdAsync(Guid id)
    {
        try
        {
            return await _refitClient.GetMutationByIdAsync(id);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Mutation>> CreateMutationAsync(MutationCreateRequest request)
    {
        try
        {
            return await _refitClient.CreateMutationAsync(request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Mutation>> CompleteMutationAsync(Guid id)
    {
        try
        {
            return await _refitClient.CompleteMutationAsync(id);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Mutation>> CancelMutationAsync(Guid id, MutationCancelRequest request)
    {
        try
        {
            return await _refitClient.CancelMutationAsync(id, request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    // === Rooms ===
    public async Task<PaginatedResponse<Room>> GetRoomsAsync(int page = 1, int page_size = 100)
    {
        try
        {
            return await _refitClient.GetRoomsAsync(page, page_size);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Room>> GetRoomByIdAsync(Guid id)
    {
        try
        {
            return await _refitClient.GetRoomByIdAsync(id);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Room>> CreateRoomAsync(RoomRequest request)
    {
        try
        {
            return await _refitClient.CreateRoomAsync(request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<Room>> UpdateRoomAsync(Guid id, RoomRequest request)
    {
        try
        {
            return await _refitClient.UpdateRoomAsync(id, request);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    public async Task<Models.ApiResponse<object>> DeleteRoomAsync(Guid id)
    {
        try
        {
            return await _refitClient.DeleteRoomAsync(id);
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    // === Health ===
    public async Task<Models.ApiResponse<object>> HealthCheckAsync()
    {
        try
        {
            return await _refitClient.HealthCheckAsync();
        }
        catch (Refit.ApiException ex)
        {
            throw await HandleApiException(ex);
        }
    }

    private async Task<Exception> HandleApiException(Refit.ApiException ex)
    {
        Log.Error(ex, "API error: {StatusCode} - {ReasonPhrase}", ex.StatusCode, ex.ReasonPhrase);

        if (ex.StatusCode == HttpStatusCode.Unauthorized)
        {
            return new SessionExpiredException();
        }

        if (ex.StatusCode == HttpStatusCode.Forbidden)
        {
            return new AuthorizationException();
        }

        try
        {
            var errorResponse = await ex.GetContentAsAsync<ErrorResponse>();
            if (errorResponse != null)
            {
                return new SimanisException(errorResponse.Message, errorResponse.ErrorCode, errorResponse.Details);
            }
        }
        catch { }

        return new ApiConnectionException($"Error: {ex.StatusCode} - {ex.ReasonPhrase}");
    }
}
