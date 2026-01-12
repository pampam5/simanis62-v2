using System.Collections.ObjectModel;
using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Win32;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk halaman laporan KIB.
/// </summary>
public partial class KibReportViewModel : ViewModelBase
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private string _selectedKategori = "B";

    [ObservableProperty]
    private string _pageTitle = "Laporan KIB B - Peralatan dan Mesin";

    [ObservableProperty]
    private string _pageSubtitle = "Format BPAD DKI Jakarta - 18 Kolom";

    [ObservableProperty]
    private ObservableCollection<Asset> _assets = new();

    [ObservableProperty]
    private int _totalCount;

    [ObservableProperty]
    private long _totalValue;

    [ObservableProperty]
    private string _loadingMessage = "Memuat data...";

    public bool CanExport => SessionService.CanExport;

    // Radio button bindings
    public bool IsKibA => SelectedKategori == "A";
    public bool IsKibB => SelectedKategori == "B";
    public bool IsKibC => SelectedKategori == "C";
    public bool IsKibD => SelectedKategori == "D";
    public bool IsKibE => SelectedKategori == "E";
    public bool IsKibF => SelectedKategori == "F";

    public List<KibKategoriInfo> KategoriOptions { get; } = new()
    {
        new("A", "KIB A - Tanah"),
        new("B", "KIB B - Peralatan dan Mesin"),
        new("C", "KIB C - Gedung dan Bangunan"),
        new("D", "KIB D - Jalan, Irigasi, Jaringan"),
        new("E", "KIB E - Aset Tetap Lainnya"),
        new("F", "KIB F - Konstruksi Dalam Pengerjaan")
    };

    public KibReportViewModel(
        IApiService apiService,
        INavigationService navigationService,
        IDialogService dialogService,
        ISessionService sessionService)
        : base(navigationService, dialogService, sessionService)
    {
        _apiService = apiService;
    }

    public override async Task OnLoadedAsync()
    {
        // Check if kategori passed as parameter
        var kategori = NavigationService.GetParameter<string>();
        if (!string.IsNullOrEmpty(kategori))
        {
            SelectedKategori = kategori;
        }

        await LoadReportAsync();
    }

    [RelayCommand]
    private async Task LoadReportAsync()
    {
        await ExecuteAsync(async () =>
        {
            Log.Information("Loading KIB report for kategori: {Kategori}", SelectedKategori);

            var response = await _apiService.GetKibReportAsync(SelectedKategori);
            if (response.Success && response.Data != null)
            {
                Assets = new ObservableCollection<Asset>(response.Data.Items);
                TotalCount = response.Data.TotalItems;
                TotalValue = response.Data.TotalNilai;

                UpdatePageTitle();
                Log.Information("KIB report loaded: {TotalItems} items", TotalCount);
            }
        });
    }

    [RelayCommand]
    private async Task ExportToExcelAsync()
    {
        if (!CanExport)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk export");
            return;
        }

        var saveDialog = new SaveFileDialog
        {
            Filter = "Excel Files (*.xlsx)|*.xlsx",
            FileName = $"KIB_{SelectedKategori}_{DateTime.Now:yyyy-MM-dd}.xlsx",
            Title = "Simpan Laporan KIB"
        };

        if (saveDialog.ShowDialog() != true) return;

        LoadingMessage = "Mengexport ke Excel...";
        await ExecuteAsync(async () =>
        {
            Log.Information("Exporting KIB {Kategori} to Excel", SelectedKategori);

            var response = await _apiService.ExportKibAsync(SelectedKategori);
            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsByteArrayAsync();
                await File.WriteAllBytesAsync(saveDialog.FileName, content);

                DialogService.ShowSnackbar($"Laporan berhasil disimpan ke {saveDialog.FileName}");
                Log.Information("KIB report exported to: {FilePath}", saveDialog.FileName);
            }
            else
            {
                SetError("Gagal mengexport laporan");
            }
        });
        LoadingMessage = "Memuat data...";
    }

    [RelayCommand]
    private async Task SelectKibAsync(string kategori)
    {
        SelectedKategori = kategori;
        await LoadReportAsync();
    }

    [RelayCommand]
    private async Task ExportAsync()
    {
        await ExportToExcelAsync();
    }

    private void UpdatePageTitle()
    {
        PageTitle = SelectedKategori switch
        {
            "A" => "Laporan KIB A - Tanah",
            "B" => "Laporan KIB B - Peralatan dan Mesin",
            "C" => "Laporan KIB C - Gedung dan Bangunan",
            "D" => "Laporan KIB D - Jalan, Irigasi, Jaringan",
            "E" => "Laporan KIB E - Aset Tetap Lainnya",
            "F" => "Laporan KIB F - Konstruksi Dalam Pengerjaan",
            _ => $"Laporan KIB {SelectedKategori}"
        };
    }

    partial void OnSelectedKategoriChanged(string value)
    {
        UpdatePageTitle();
        OnPropertyChanged(nameof(IsKibA));
        OnPropertyChanged(nameof(IsKibB));
        OnPropertyChanged(nameof(IsKibC));
        OnPropertyChanged(nameof(IsKibD));
        OnPropertyChanged(nameof(IsKibE));
        OnPropertyChanged(nameof(IsKibF));
    }
}

public record KibKategoriInfo(string Value, string Display);
