using System.Net.Http;
using Refit;
using Simanis62.Models;
using ApiResponse = Simanis62.Models.ApiResponse<object>;

namespace Simanis62.Services.Interfaces;

/// <summary>
/// Refit interface untuk API calls.
/// </summary>
public interface IApiService
{
    // === Auth ===
    [Post("/api/v1/auth/login")]
    Task<Models.ApiResponse<LoginResponse>> LoginAsync([Body] LoginRequest request);

    [Post("/api/v1/auth/logout")]
    Task<Models.ApiResponse<object>> LogoutAsync();

    [Get("/api/v1/auth/me")]
    Task<Models.ApiResponse<User>> GetCurrentUserAsync();

    // === Assets ===
    [Get("/api/v1/aset")]
    Task<PaginatedResponse<Asset>> GetAssetsAsync(
        [Query] string? keyword = null,
        [Query] string? kategori_kib = null,
        [Query] string? status = null,
        [Query] Guid? ruangan_id = null,
        [Query] int page = 1,
        [Query] int page_size = 100);

    [Get("/api/v1/aset/{id}")]
    Task<Models.ApiResponse<Asset>> GetAssetByIdAsync(Guid id);

    [Post("/api/v1/aset")]
    Task<Models.ApiResponse<Asset>> CreateAssetAsync([Body] AssetRequest request);

    [Put("/api/v1/aset/{id}")]
    Task<Models.ApiResponse<Asset>> UpdateAssetAsync(Guid id, [Body] AssetRequest request);

    [Delete("/api/v1/aset/{id}")]
    Task<Models.ApiResponse<object>> DeleteAssetAsync(Guid id, [Body] AssetDeleteRequest request);

    // === KIB Reports ===
    [Get("/api/v1/kib/{kategori}")]
    Task<Models.ApiResponse<KibReportResponse>> GetKibReportAsync(string kategori);

    [Get("/api/v1/kib/{kategori}/export")]
    Task<HttpResponseMessage> ExportKibAsync(string kategori);

    // === Mutations ===
    [Get("/api/v1/mutasi")]
    Task<PaginatedResponse<Mutation>> GetMutationsAsync(
        [Query] string? status = null,
        [Query] int page = 1,
        [Query] int page_size = 100);

    [Get("/api/v1/mutasi/{id}")]
    Task<Models.ApiResponse<Mutation>> GetMutationByIdAsync(Guid id);

    [Post("/api/v1/mutasi")]
    Task<Models.ApiResponse<Mutation>> CreateMutationAsync([Body] MutationCreateRequest request);

    [Put("/api/v1/mutasi/{id}/complete")]
    Task<Models.ApiResponse<Mutation>> CompleteMutationAsync(Guid id);

    [Put("/api/v1/mutasi/{id}/cancel")]
    Task<Models.ApiResponse<Mutation>> CancelMutationAsync(Guid id, [Body] MutationCancelRequest request);

    // === Rooms ===
    [Get("/api/v1/ruangan")]
    Task<PaginatedResponse<Room>> GetRoomsAsync(
        [Query] int page = 1,
        [Query] int page_size = 100);

    [Get("/api/v1/ruangan/{id}")]
    Task<Models.ApiResponse<Room>> GetRoomByIdAsync(Guid id);

    [Post("/api/v1/ruangan")]
    Task<Models.ApiResponse<Room>> CreateRoomAsync([Body] RoomRequest request);

    [Put("/api/v1/ruangan/{id}")]
    Task<Models.ApiResponse<Room>> UpdateRoomAsync(Guid id, [Body] RoomRequest request);

    [Delete("/api/v1/ruangan/{id}")]
    Task<Models.ApiResponse<object>> DeleteRoomAsync(Guid id);

    // === Health ===
    [Get("/api/v1/health")]
    Task<Models.ApiResponse<object>> HealthCheckAsync();
}
