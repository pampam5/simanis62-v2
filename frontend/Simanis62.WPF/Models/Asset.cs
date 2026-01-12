namespace Simanis62.Models;

/// <summary>
/// Model untuk data aset.
/// </summary>
public class Asset
{
    public Guid Id { get; set; }
    public int NomorRegister { get; set; }
    public string KodeBarang { get; set; } = string.Empty;
    public string NamaBarang { get; set; } = string.Empty;
    public string KategoriKib { get; set; } = "B";
    public string Status { get; set; } = "Aktif";
    public string Kondisi { get; set; } = "Baik";
    public long Harga { get; set; }
    public int TahunPerolehan { get; set; }
    public string? AsalPerolehan { get; set; }
    public string? Keterangan { get; set; }

    // Foreign keys
    public Guid? RuanganId { get; set; }
    public string? NamaRuangan { get; set; }

    // KIB B specific fields
    public string? Merk { get; set; }
    public string? Tipe { get; set; }
    public string? UkuranCc { get; set; }
    public string? Satuan { get; set; }
    public string? NomorRangka { get; set; }
    public string? NomorMesin { get; set; }
    public string? NomorPolisi { get; set; }
    public string? NomorBpkb { get; set; }
    public string? Bahan { get; set; }

    // Audit fields
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    public Guid? CreatedBy { get; set; }
    public Guid? UpdatedBy { get; set; }

    /// <summary>
    /// Format harga ke Rupiah.
    /// </summary>
    public string HargaFormatted => $"Rp {Harga:N0}";
}

/// <summary>
/// Request untuk create/update aset.
/// </summary>
public class AssetRequest
{
    public string KodeBarang { get; set; } = string.Empty;
    public string NamaBarang { get; set; } = string.Empty;
    public string KategoriKib { get; set; } = "B";
    public string Kondisi { get; set; } = "Baik";
    public long Harga { get; set; }
    public int TahunPerolehan { get; set; }
    public string? AsalPerolehan { get; set; }
    public string? Keterangan { get; set; }
    public Guid? RuanganId { get; set; }

    // KIB B specific
    public string? Merk { get; set; }
    public string? Tipe { get; set; }
    public string? UkuranCc { get; set; }
    public string? Satuan { get; set; }
    public string? NomorRangka { get; set; }
    public string? NomorMesin { get; set; }
    public string? NomorPolisi { get; set; }
    public string? NomorBpkb { get; set; }
    public string? Bahan { get; set; }
}

/// <summary>
/// Request untuk delete aset.
/// </summary>
public class AssetDeleteRequest
{
    public string DeleteReason { get; set; } = string.Empty;
}

/// <summary>
/// Parameter untuk search aset.
/// </summary>
public class AssetSearchParams
{
    public string? Keyword { get; set; }
    public string? KategoriKib { get; set; }
    public string? Status { get; set; }
    public Guid? RuanganId { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 100;
}
