using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk halaman dashboard.
/// </summary>
public partial class DashboardViewModel : ViewModelBase
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private int _totalAset;

    [ObservableProperty]
    private string _totalNilai = "Rp 0";

    [ObservableProperty]
    private int _totalRuangan;

    [ObservableProperty]
    private int _mutasiPending;

    [ObservableProperty]
    private int _asetKibA;

    [ObservableProperty]
    private int _asetKibB;

    [ObservableProperty]
    private int _asetKibC;

    [ObservableProperty]
    private int _asetKibD;

    [ObservableProperty]
    private int _asetKibE;

    [ObservableProperty]
    private int _asetKibF;

    [ObservableProperty]
    private int _asetAktif;

    [ObservableProperty]
    private int _asetRusak;

    [ObservableProperty]
    private int _asetMutasi;

    public DashboardViewModel(
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
        await LoadDashboardDataAsync();
    }

    [RelayCommand]
    private async Task RefreshAsync()
    {
        await LoadDashboardDataAsync();
    }

    private async Task LoadDashboardDataAsync()
    {
        await ExecuteAsync(async () =>
        {
            Log.Information("Loading dashboard data...");

            // Load assets count per category
            var kibCategories = new[] { "A", "B", "C", "D", "E", "F" };
            long totalNilai = 0;
            int totalAset = 0;

            foreach (var kategori in kibCategories)
            {
                var response = await _apiService.GetKibReportAsync(kategori);
                if (response.Success && response.Data != null)
                {
                    var count = response.Data.TotalItems;
                    totalAset += count;
                    totalNilai += response.Data.TotalNilai;

                    switch (kategori)
                    {
                        case "A": AsetKibA = count; break;
                        case "B": AsetKibB = count; break;
                        case "C": AsetKibC = count; break;
                        case "D": AsetKibD = count; break;
                        case "E": AsetKibE = count; break;
                        case "F": AsetKibF = count; break;
                    }
                }
            }

            TotalAset = totalAset;
            TotalNilai = $"Rp {totalNilai:N0}";

            // Load rooms count
            var roomsResponse = await _apiService.GetRoomsAsync(1, 1);
            if (roomsResponse.Success)
            {
                TotalRuangan = roomsResponse.Total;
            }

            // Load pending mutations
            var mutationsResponse = await _apiService.GetMutationsAsync("Dalam_Proses", 1, 1);
            if (mutationsResponse.Success)
            {
                MutasiPending = mutationsResponse.Total;
            }

            // Load assets by status
            var activeResponse = await _apiService.GetAssetsAsync(status: "Aktif", page_size: 1);
            if (activeResponse.Success) AsetAktif = activeResponse.Total;

            var rusakResponse = await _apiService.GetAssetsAsync(status: "Rusak", page_size: 1);
            if (rusakResponse.Success) AsetRusak = rusakResponse.Total;

            var mutasiResponse = await _apiService.GetAssetsAsync(status: "Mutasi", page_size: 1);
            if (mutasiResponse.Success) AsetMutasi = mutasiResponse.Total;

            Log.Information("Dashboard data loaded: {TotalAset} assets, {TotalRuangan} rooms", TotalAset, TotalRuangan);
        });
    }

    [RelayCommand]
    private void NavigateToAssets()
    {
        NavigationService.NavigateTo("AssetList");
    }

    [RelayCommand]
    private void NavigateToKibReport(string kategori)
    {
        NavigationService.NavigateTo("KibReport", kategori);
    }

    [RelayCommand]
    private void NavigateToMutations()
    {
        NavigationService.NavigateTo("Mutation");
    }
}
