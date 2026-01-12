namespace Simanis62.Models;

/// <summary>
/// Model untuk data mutasi.
/// </summary>
public class Mutation
{
    public Guid Id { get; set; }
    public Guid AsetId { get; set; }
    public string? NamaAset { get; set; }
    public Guid RuanganAsalId { get; set; }
    public string? NamaRuanganAsal { get; set; }
    public Guid RuanganTujuanId { get; set; }
    public string? NamaRuanganTujuan { get; set; }
    public Guid UserId { get; set; }
    public string? NamaUser { get; set; }
    public string Alasan { get; set; } = string.Empty;
    public DateTime TanggalMutasi { get; set; }
    public string KondisiSaatMutasi { get; set; } = "Baik";
    public string StatusMutasi { get; set; } = "Dalam_Proses";
    public DateTime MulaiMutasi { get; set; }
    public DateTime? SelesaiMutasi { get; set; }
    public string? AlasanPembatalan { get; set; }
    public DateTime CreatedAt { get; set; }

    /// <summary>
    /// Status display text.
    /// </summary>
    public string StatusDisplay => StatusMutasi switch
    {
        "Dalam_Proses" => "Dalam Proses",
        "Selesai" => "Selesai",
        "Dibatalkan" => "Dibatalkan",
        _ => StatusMutasi
    };
}

/// <summary>
/// Request untuk create mutasi.
/// </summary>
public class MutationCreateRequest
{
    public Guid AsetId { get; set; }
    public Guid RuanganTujuanId { get; set; }
    public string Alasan { get; set; } = string.Empty;
    public DateTime TanggalMutasi { get; set; } = DateTime.Today;
    public string KondisiSaatMutasi { get; set; } = "Baik";
}

/// <summary>
/// Request untuk cancel mutasi.
/// </summary>
public class MutationCancelRequest
{
    public string AlasanPembatalan { get; set; } = string.Empty;
}
