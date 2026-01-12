namespace Simanis62.Models;

/// <summary>
/// Model untuk data ruangan.
/// </summary>
public class Room
{
    public Guid Id { get; set; }
    public string KodeRuangan { get; set; } = string.Empty;
    public string NamaRuangan { get; set; } = string.Empty;
    public string? Keterangan { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    /// <summary>
    /// Display text untuk ComboBox.
    /// </summary>
    public string DisplayText => $"{KodeRuangan} - {NamaRuangan}";
}

/// <summary>
/// Request untuk create/update ruangan.
/// </summary>
public class RoomRequest
{
    public string KodeRuangan { get; set; } = string.Empty;
    public string NamaRuangan { get; set; } = string.Empty;
    public string? Keterangan { get; set; }
}
