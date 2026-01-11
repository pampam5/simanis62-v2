---
inclusion: fileMatch
fileMatchPattern: "**/*.cs,**/*.xaml"
---

# Standar WPF .NET 8 - SIMANIS62 V2

## Gaya Kode C#

### Naming Convention
```csharp
// Private fields: _camelCase
private string _namaBarang = string.Empty;
private readonly IApiService _apiService;

// Public properties: PascalCase
public string NamaBarang { get; set; }
public ObservableCollection<Aset> DaftarAset { get; }

// Methods: PascalCase
public async Task LoadDataAsync() { }
private void ValidateInput() { }
```

### Nullable Reference Types (WAJIB)
```csharp
// ✅ BENAR - Nullable explicit
public string? Keterangan { get; set; }
public Aset? SelectedAset { get; set; }

// ✅ BENAR - Non-nullable dengan default
public string NamaBarang { get; set; } = string.Empty;
public List<Aset> DaftarAset { get; } = new();
```

## MVVM Pattern dengan CommunityToolkit

### ViewModel Structure
```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class AsetListViewModel : ObservableObject
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private string _searchQuery = string.Empty;

    [ObservableProperty]
    private bool _isLoading;

    [ObservableProperty]
    private Aset? _selectedAset;

    public ObservableCollection<Aset> DaftarAset { get; } = new();

    public AsetListViewModel(IApiService apiService)
    {
        _apiService = apiService;
    }

    [RelayCommand]
    private async Task LoadDataAsync()
    {
        IsLoading = true;
        try
        {
            var result = await _apiService.GetAsetListAsync();
            DaftarAset.Clear();
            foreach (var aset in result.Data)
            {
                DaftarAset.Add(aset);
            }
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task SearchAsync()
    {
        // Implementasi search
    }
}
```

## XAML dengan MaterialDesign

### View Structure
```xml
<UserControl x:Class="Simanis62.WPF.Views.AsetListView"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:md="http://materialdesigninxaml.net/winfx/xaml/themes"
             xmlns:vm="clr-namespace:Simanis62.WPF.ViewModels">

    <UserControl.DataContext>
        <vm:AsetListViewModel />
    </UserControl.DataContext>

    <Grid>
        <!-- Search Bar -->
        <md:Card Margin="16">
            <StackPanel Orientation="Horizontal">
                <TextBox Text="{Binding SearchQuery, UpdateSourceTrigger=PropertyChanged}"
                         md:HintAssist.Hint="Cari aset..."
                         Width="300" />
                <Button Command="{Binding SearchCommand}"
                        Style="{StaticResource MaterialDesignFlatButton}">
                    <md:PackIcon Kind="Search" />
                </Button>
            </StackPanel>
        </md:Card>

        <!-- Data Grid -->
        <DataGrid ItemsSource="{Binding DaftarAset}"
                  SelectedItem="{Binding SelectedAset}"
                  AutoGenerateColumns="False"
                  IsReadOnly="True">
            <DataGrid.Columns>
                <DataGridTextColumn Header="Kode" Binding="{Binding KodeBarang}" />
                <DataGridTextColumn Header="Nama Barang" Binding="{Binding NamaBarang}" />
                <DataGridTextColumn Header="Harga" Binding="{Binding Harga, StringFormat=Rp {0:N0}}" />
                <DataGridTextColumn Header="Status" Binding="{Binding Status}" />
            </DataGrid.Columns>
        </DataGrid>

        <!-- Loading Indicator -->
        <md:ProgressBar IsIndeterminate="True"
                        Visibility="{Binding IsLoading, Converter={StaticResource BoolToVisibility}}" />
    </Grid>
</UserControl>
```

## API Service dengan Refit

```csharp
using Refit;

public interface IApiService
{
    [Get("/api/v1/aset")]
    Task<ApiResponse<List<Aset>>> GetAsetListAsync(
        [Query] int page = 1,
        [Query] int limit = 100);

    [Get("/api/v1/aset/{id}")]
    Task<ApiResponse<Aset>> GetAsetByIdAsync(Guid id);

    [Post("/api/v1/aset")]
    Task<ApiResponse<Aset>> CreateAsetAsync([Body] AsetCreate data);

    [Put("/api/v1/aset/{id}")]
    Task<ApiResponse<Aset>> UpdateAsetAsync(Guid id, [Body] AsetUpdate data);

    [Delete("/api/v1/aset/{id}")]
    Task<ApiResponse<object>> DeleteAsetAsync(Guid id);
}
```

## Error Handling

```csharp
try
{
    var result = await _apiService.GetAsetListAsync();
    if (result.Success)
    {
        // Handle success
    }
    else
    {
        // Handle API error
        await ShowErrorAsync(result.Error?.Message ?? "Terjadi kesalahan");
    }
}
catch (ApiException ex)
{
    // Handle HTTP error
    await ShowErrorAsync($"Error: {ex.StatusCode}");
}
catch (Exception ex)
{
    // Handle unexpected error
    await ShowErrorAsync("Terjadi kesalahan tidak terduga");
}
```

## Referensi

#[[file:docs/tech_stack.md]]

## Crash Reporting & Logging (Serilog + GlitchTip)

### Setup di App.xaml.cs
```csharp
using Serilog;
using Sentry;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        // Setup Serilog dengan Sentry sink
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Information()
            .WriteTo.File(
                path: "logs/simanis62-wpf.log",
                rollingInterval: RollingInterval.Day,
                retainedFileCountLimit: 7,
                outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} [{Level}] {Message}{NewLine}{Exception}")
            .WriteTo.Sentry(o =>
            {
                o.Dsn = Environment.GetEnvironmentVariable("GLITCHTIP_DSN");
                o.MinimumEventLevel = Serilog.Events.LogEventLevel.Error;
            })
            .CreateLogger();

        // Global exception handler
        AppDomain.CurrentDomain.UnhandledException += (s, args) =>
        {
            var ex = (Exception)args.ExceptionObject;
            Log.Fatal(ex, "Unhandled exception");
            SentrySdk.CaptureException(ex);
        };

        DispatcherUnhandledException += (s, args) =>
        {
            Log.Error(args.Exception, "Dispatcher unhandled exception");
            SentrySdk.CaptureException(args.Exception);
            args.Handled = true; // Prevent crash, show error dialog
        };

        base.OnStartup(e);
    }

    protected override void OnExit(ExitEventArgs e)
    {
        Log.CloseAndFlush();
        base.OnExit(e);
    }
}
```

### Penggunaan di ViewModel
```csharp
using Serilog;

public partial class AsetListViewModel : ObservableObject
{
    [RelayCommand]
    private async Task LoadDataAsync()
    {
        Log.Information("Loading aset list...");
        IsLoading = true;

        try
        {
            var result = await _apiService.GetAsetListAsync();
            Log.Information("Loaded {Count} aset", result.Data.Count);

            DaftarAset.Clear();
            foreach (var aset in result.Data)
            {
                DaftarAset.Add(aset);
            }
        }
        catch (ApiException ex)
        {
            Log.Error(ex, "API error loading aset: {StatusCode}", ex.StatusCode);
            await ShowErrorAsync($"Gagal memuat data: {ex.StatusCode}");
        }
        catch (Exception ex)
        {
            Log.Error(ex, "Unexpected error loading aset");
            SentrySdk.CaptureException(ex); // Kirim ke GlitchTip
            await ShowErrorAsync("Terjadi kesalahan tidak terduga");
        }
        finally
        {
            IsLoading = false;
        }
    }
}
```

### NuGet Packages Required
```xml
<PackageReference Include="Serilog" Version="3.*" />
<PackageReference Include="Serilog.Sinks.File" Version="5.*" />
<PackageReference Include="Serilog.Sinks.Sentry" Version="4.*" />
<PackageReference Include="Sentry" Version="4.*" />
```

### Yang TIDAK BOLEH Di-log
```csharp
// ❌ SALAH - Log password
Log.Information("Login: {Username}, {Password}", username, password);

// ✅ BENAR - Tanpa password
Log.Information("Login attempt: {Username}", username);

// ❌ SALAH - Log data sensitif
Log.Information("Aset: {@Aset}", aset);

// ✅ BENAR - Hanya ID
Log.Information("Aset loaded: {AsetId}", aset.Id);
```
