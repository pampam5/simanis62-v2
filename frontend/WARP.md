# WARP.md - Frontend (WPF .NET 8)
# Aturan spesifik untuk folder frontend/

## Tech Stack

- .NET 8 (WPF)
- MVVM CommunityToolkit
- Refit (HTTP client)
- Polly (resilience)
- MaterialDesignInXaml (UI)
- Serilog (logging)

## Perintah

```bash
# Build & Test
dotnet restore
dotnet build
dotnet test

# Publish
dotnet publish -c Release -r win-x64 --self-contained
```

## Struktur

```
Simanis62.WPF/
├── Views/          # XAML views
├── ViewModels/     # MVVM ViewModels
├── Models/         # Data models (mirror API)
├── Services/       # API clients, logging
└── Converters/     # Value converters
```

## Konvensi Kode

- **Nullable reference types** enabled
- **PascalCase** untuk public members
- **_camelCase** untuk private fields
- XAML: Gunakan **MaterialDesign** components

## Contoh Pattern

```csharp
public partial class AsetViewModel : ObservableObject
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private string _namaBarang = string.Empty;

    [ObservableProperty]
    private bool _isLoading;

    [RelayCommand]
    private async Task LoadAsetAsync()
    {
        IsLoading = true;
        try
        {
            var result = await _apiService.GetAsetAsync();
            // Process result
        }
        finally
        {
            IsLoading = false;
        }
    }
}
```

## API Client (Refit)

```csharp
public interface IApiService
{
    [Get("/api/v1/aset")]
    Task<ApiResponse<List<Aset>>> GetAsetAsync();

    [Post("/api/v1/aset")]
    Task<ApiResponse<Aset>> CreateAsetAsync([Body] AsetCreate data);
}
```

## Error Handling

- Gunakan Polly untuk retry policies
- Log errors ke Serilog + GlitchTip
- Show user-friendly messages (Bahasa Indonesia)

## UI Messages (Bahasa Indonesia)

```csharp
// ✅ BENAR
MessageBox.Show("Aset berhasil disimpan");
MessageBox.Show("Gagal menyimpan data. Silakan coba lagi.");

// ❌ SALAH
MessageBox.Show("Asset saved successfully");
```

## 🚫 JANGAN

- Gunakan Entity Framework (backend pakai SQLModel)
- Hardcode API URL (pakai config)
- Block UI thread untuk async operations
- Log data sensitif

---

*Referensi: `frontend/AGENTS.md`, `.kiro/steering/wpf-standards.md`*
