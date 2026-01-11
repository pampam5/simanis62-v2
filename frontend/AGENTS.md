# AGENTS.md - Frontend

**Tech Stack**: WPF .NET 8, MVVM CommunityToolkit, MaterialDesignInXaml

---

## Aturan Khusus

### MVVM Pattern (WAJIB)
- Gunakan `[ObservableProperty]` untuk properties
- Gunakan `[RelayCommand]` untuk commands
- ViewModel TIDAK boleh reference View langsung
- Gunakan **Dependency Injection** untuk services

### Konvensi Penamaan

| Konteks | Konvensi | Bahasa | Contoh |
|---------|----------|--------|--------|
| Class names | PascalCase | English | `AsetViewModel`, `LoginView` |
| Private fields | _camelCase | English | `_namaBarang`, `_isLoading` |
| Public properties | PascalCase | English | `NamaBarang`, `IsLoading` |
| Methods | PascalCase | English | `GetAssetById()`, `SaveAsync()` |
| UI Labels | - | **Bahasa Indonesia** | `"Nama Barang"`, `"Simpan"` |
| Error messages | - | **Bahasa Indonesia** | `"Aset tidak ditemukan"` |

### Contoh ViewModel

```csharp
public partial class AsetViewModel : ObservableObject
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private string _namaBarang = string.Empty;

    [ObservableProperty]
    private int _harga; // Rupiah penuh, BUKAN ribuan

    [ObservableProperty]
    private string _kondisi = "Baik";

    [ObservableProperty]
    private bool _isLoading;

    public AsetViewModel(IApiService apiService)
    {
        _apiService = apiService;
    }

    [RelayCommand]
    private async Task SimpanAsetAsync()
    {
        IsLoading = true;
        try
        {
            await _apiService.CreateAsetAsync(/* ... */);
        }
        finally
        {
            IsLoading = false;
        }
    }
}
```

### Authorization di UI

```csharp
// Cek role untuk tampilkan/sembunyikan tombol
public bool CanEdit => CurrentUser.Role == "Admin";
public bool CanExport => CurrentUser.Role == "Admin" || CurrentUser.DapatEkspor;

// Kepala Sekolah = Viewer dengan DapatEkspor=true
// Sembunyikan tombol Edit/Delete untuk non-Admin
// Tampilkan tombol Export untuk Admin dan user dengan DapatEkspor=true
```

### API Client dengan Refit

```csharp
public interface IApiService
{
    [Get("/api/v1/aset")]
    Task<List<Aset>> GetAllAsetAsync();

    [Get("/api/v1/aset/{id}")]
    Task<Aset> GetAsetByIdAsync(Guid id);

    [Post("/api/v1/aset")]
    Task<Aset> CreateAsetAsync([Body] AsetCreate aset);
}
```

### UI Components (MaterialDesign)

- Gunakan `MaterialDesignThemes` untuk styling
- Gunakan `DialogHost` untuk dialogs
- Gunakan `Snackbar` untuk notifications
- Semua text UI dalam **Bahasa Indonesia**

---

*Sinkronisasi dengan: Root AGENTS.md v1.6*
