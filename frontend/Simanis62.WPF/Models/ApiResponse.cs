using System.Text.Json.Serialization;

namespace Simanis62.Models;

/// <summary>
/// Standard API response wrapper.
/// </summary>
public class ApiResponse<T>
{
    [JsonPropertyName("success")]
    public bool Success { get; set; }

    [JsonPropertyName("data")]
    public T? Data { get; set; }

    [JsonPropertyName("message")]
    public string? Message { get; set; }

    [JsonPropertyName("correlation_id")]
    public string? CorrelationId { get; set; }
}

/// <summary>
/// Standard error response.
/// </summary>
public class ErrorResponse
{
    [JsonPropertyName("success")]
    public bool Success { get; set; }

    [JsonPropertyName("error_code")]
    public string ErrorCode { get; set; } = string.Empty;

    [JsonPropertyName("message")]
    public string Message { get; set; } = string.Empty;

    [JsonPropertyName("details")]
    public Dictionary<string, object>? Details { get; set; }

    [JsonPropertyName("correlation_id")]
    public string? CorrelationId { get; set; }
}

/// <summary>
/// Paginated response.
/// </summary>
public class PaginatedResponse<T>
{
    [JsonPropertyName("success")]
    public bool Success { get; set; }

    [JsonPropertyName("data")]
    public List<T> Data { get; set; } = new();

    [JsonPropertyName("total")]
    public int Total { get; set; }

    [JsonPropertyName("page")]
    public int Page { get; set; }

    [JsonPropertyName("page_size")]
    public int PageSize { get; set; }

    [JsonPropertyName("total_pages")]
    public int TotalPages { get; set; }

    [JsonPropertyName("correlation_id")]
    public string? CorrelationId { get; set; }
}

/// <summary>
/// KIB Report response.
/// </summary>
public class KibReportResponse
{
    [JsonPropertyName("kategori")]
    public string Kategori { get; set; } = string.Empty;

    [JsonPropertyName("total_items")]
    public int TotalItems { get; set; }

    [JsonPropertyName("total_nilai")]
    public long TotalNilai { get; set; }

    [JsonPropertyName("items")]
    public List<Asset> Items { get; set; } = new();

    /// <summary>
    /// Format total nilai ke Rupiah.
    /// </summary>
    public string TotalNilaiFormatted => $"Rp {TotalNilai:N0}";
}

/// <summary>
/// Dashboard statistics.
/// </summary>
public class DashboardStats
{
    public int TotalAset { get; set; }
    public long TotalNilai { get; set; }
    public int TotalRuangan { get; set; }
    public int MutasiPending { get; set; }
    public Dictionary<string, int> AsetPerKategori { get; set; } = new();
    public Dictionary<string, int> AsetPerStatus { get; set; } = new();

    public string TotalNilaiFormatted => $"Rp {TotalNilai:N0}";
}
