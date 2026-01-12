using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk halaman daftar aset.
/// </summary>
public partial class AssetListViewModel : ViewModelBase
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private ObservableCollection<Asset> _assets = new();

    [ObservableProperty]
    private Asset? _selectedAsset;

    [ObservableProperty]
    private string _searchKeyword = string.Empty;

    [ObservableProperty]
    private string? _selectedKategori;

    [ObservableProperty]
    private string? _selectedStatus;

    [ObservableProperty]
    private Room? _selectedRuangan;

    [ObservableProperty]
    private ObservableCollection<Room> _rooms = new();

    [ObservableProperty]
    private int _currentPage = 1;

    [ObservableProperty]
    private int _totalPages = 1;

    [ObservableProperty]
    private int _totalItems;

    [ObservableProperty]
    private int _pageSize = 100;

    public bool CanEdit => SessionService.IsAdmin;
    public bool CanDelete => SessionService.IsAdmin;

    public List<string> KategoriOptions { get; } = new() { "", "A", "B", "C", "D", "E", "F" };
    public List<string> StatusOptions { get; } = new() { "", "Aktif", "Rusak", "Mutasi", "Dihapus" };

    public AssetListViewModel(
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
        await LoadRoomsAsync();
        await SearchAsync();
    }

    private async Task LoadRoomsAsync()
    {
        var response = await _apiService.GetRoomsAsync(1, 1000);
        if (response.Success)
        {
            Rooms = new ObservableCollection<Room>(response.Data);
        }
    }

    [RelayCommand]
    private async Task SearchAsync()
    {
        await ExecuteAsync(async () =>
        {
            Log.Information("Searching assets: keyword={Keyword}, kategori={Kategori}, status={Status}",
                SearchKeyword, SelectedKategori, SelectedStatus);

            var response = await _apiService.GetAssetsAsync(
                keyword: string.IsNullOrWhiteSpace(SearchKeyword) ? null : SearchKeyword,
                kategori_kib: string.IsNullOrWhiteSpace(SelectedKategori) ? null : SelectedKategori,
                status: string.IsNullOrWhiteSpace(SelectedStatus) ? null : SelectedStatus,
                ruangan_id: SelectedRuangan?.Id,
                page: CurrentPage,
                page_size: PageSize);

            if (response.Success)
            {
                Assets = new ObservableCollection<Asset>(response.Data);
                TotalItems = response.Total;
                TotalPages = response.TotalPages;
                CurrentPage = response.Page;
            }
        });
    }

    [RelayCommand]
    private void ClearFilters()
    {
        SearchKeyword = string.Empty;
        SelectedKategori = null;
        SelectedStatus = null;
        SelectedRuangan = null;
        CurrentPage = 1;
    }

    [RelayCommand]
    private async Task NextPageAsync()
    {
        if (CurrentPage < TotalPages)
        {
            CurrentPage++;
            await SearchAsync();
        }
    }

    [RelayCommand]
    private async Task PreviousPageAsync()
    {
        if (CurrentPage > 1)
        {
            CurrentPage--;
            await SearchAsync();
        }
    }

    [RelayCommand]
    private void CreateAsset()
    {
        if (!CanEdit)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk menambah aset");
            return;
        }
        NavigationService.NavigateTo("AssetForm");
    }

    [RelayCommand]
    private void EditAsset(Asset? asset)
    {
        if (!CanEdit)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk mengedit aset");
            return;
        }
        if (asset != null)
        {
            NavigationService.NavigateTo("AssetForm", asset);
        }
    }

    [RelayCommand]
    private async Task DeleteAssetAsync(Asset? asset)
    {
        if (!CanDelete)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk menghapus aset");
            return;
        }

        if (asset == null) return;

        var reason = await DialogService.ShowInputAsync(
            "Hapus Aset",
            $"Masukkan alasan penghapusan aset '{asset.NamaBarang}':\n(minimal 20 karakter)");

        if (string.IsNullOrWhiteSpace(reason)) return;

        if (reason.Length < 20)
        {
            await DialogService.ShowWarningAsync("Validasi", "Alasan penghapusan minimal 20 karakter");
            return;
        }

        var confirm = await DialogService.ShowConfirmAsync(
            "Konfirmasi Hapus",
            $"Apakah Anda yakin ingin menghapus aset '{asset.NamaBarang}'?");

        if (!confirm) return;

        await ExecuteAsync(async () =>
        {
            var response = await _apiService.DeleteAssetAsync(asset.Id, new AssetDeleteRequest { DeleteReason = reason });
            if (response.Success)
            {
                DialogService.ShowSnackbar("Aset berhasil dihapus");
                await SearchAsync();
            }
        });
    }

    [RelayCommand]
    private void ViewAssetDetail(Asset? asset)
    {
        if (asset != null)
        {
            NavigationService.NavigateTo("AssetForm", asset);
        }
    }

    partial void OnSearchKeywordChanged(string value)
    {
        CurrentPage = 1;
    }

    partial void OnSelectedKategoriChanged(string? value)
    {
        CurrentPage = 1;
    }

    partial void OnSelectedStatusChanged(string? value)
    {
        CurrentPage = 1;
    }
}
