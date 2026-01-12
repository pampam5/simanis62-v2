using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk halaman mutasi aset.
/// </summary>
public partial class MutationViewModel : ViewModelBase
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private ObservableCollection<Mutation> _mutations = new();

    [ObservableProperty]
    private Mutation? _selectedMutation;

    [ObservableProperty]
    private string? _selectedStatus;

    [ObservableProperty]
    private int _currentPage = 1;

    [ObservableProperty]
    private int _totalPages = 1;

    [ObservableProperty]
    private int _totalItems;

    // Form fields for new mutation
    [ObservableProperty]
    private bool _isFormVisible;

    [ObservableProperty]
    private ObservableCollection<Asset> _availableAssets = new();

    [ObservableProperty]
    private Asset? _selectedAsset;

    [ObservableProperty]
    private ObservableCollection<Room> _rooms = new();

    [ObservableProperty]
    private Room? _selectedRuanganTujuan;

    [ObservableProperty]
    private string _alasan = string.Empty;

    [ObservableProperty]
    private DateTime _tanggalMutasi = DateTime.Today;

    [ObservableProperty]
    private string _selectedKondisi = "Baik";

    public bool CanManage => SessionService.IsAdmin;
    public bool CanCreate => SessionService.IsAdmin;
    public bool CanModify => SessionService.IsAdmin && SelectedMutation?.StatusMutasi == "Dalam_Proses";
    public bool CanComplete => SessionService.IsAdmin && SelectedMutation?.StatusMutasi == "Dalam_Proses";
    public bool CanCancel => SessionService.IsAdmin && SelectedMutation?.StatusMutasi == "Dalam_Proses";
    public bool HasSelection => SelectedMutation != null;
    public bool HasNoSelection => SelectedMutation == null;

    // Filter bindings
    public bool ShowAll => string.IsNullOrEmpty(SelectedStatus);
    public bool ShowPending => SelectedStatus == "Dalam_Proses";
    public bool ShowCompleted => SelectedStatus == "Selesai";
    public bool ShowCancelled => SelectedStatus == "Dibatalkan";

    public List<string> StatusOptions { get; } = new() { "", "Dalam_Proses", "Selesai", "Dibatalkan" };
    public List<string> KondisiOptions { get; } = new() { "Baik", "Rusak_Ringan", "Rusak_Berat" };

    public MutationViewModel(
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
        await LoadDataAsync();
    }

    private async Task LoadDataAsync()
    {
        await LoadMutationsAsync();
        await LoadRoomsAsync();
        await LoadAvailableAssetsAsync();
    }

    [RelayCommand]
    private async Task LoadMutationsAsync()
    {
        await ExecuteAsync(async () =>
        {
            Log.Information("Loading mutations: status={Status}", SelectedStatus);

            var response = await _apiService.GetMutationsAsync(
                status: string.IsNullOrWhiteSpace(SelectedStatus) ? null : SelectedStatus,
                page: CurrentPage);

            if (response.Success)
            {
                Mutations = new ObservableCollection<Mutation>(response.Data);
                TotalItems = response.Total;
                TotalPages = response.TotalPages;
            }
        });
    }

    private async Task LoadRoomsAsync()
    {
        var response = await _apiService.GetRoomsAsync(1, 1000);
        if (response.Success)
        {
            Rooms = new ObservableCollection<Room>(response.Data);
        }
    }

    private async Task LoadAvailableAssetsAsync()
    {
        // Load assets that are not in mutation status
        var response = await _apiService.GetAssetsAsync(status: "Aktif", page_size: 1000);
        if (response.Success)
        {
            AvailableAssets = new ObservableCollection<Asset>(response.Data);
        }
    }

    [RelayCommand]
    private void ShowCreateForm()
    {
        if (!CanManage)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk membuat mutasi");
            return;
        }

        ClearForm();
        IsFormVisible = true;
    }

    [RelayCommand]
    private void HideForm()
    {
        IsFormVisible = false;
        ClearForm();
    }

    private void ClearForm()
    {
        SelectedAsset = null;
        SelectedRuanganTujuan = null;
        Alasan = string.Empty;
        TanggalMutasi = DateTime.Today;
        SelectedKondisi = "Baik";
    }

    [RelayCommand]
    private async Task CreateMutationAsync()
    {
        if (!CanManage)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk membuat mutasi");
            return;
        }

        // Validate
        if (SelectedAsset == null)
        {
            SetError("Pilih aset yang akan dimutasi");
            return;
        }

        if (SelectedRuanganTujuan == null)
        {
            SetError("Pilih ruangan tujuan");
            return;
        }

        if (SelectedAsset.RuanganId == SelectedRuanganTujuan.Id)
        {
            SetError("Ruangan tujuan tidak boleh sama dengan ruangan asal");
            return;
        }

        if (string.IsNullOrWhiteSpace(Alasan) || Alasan.Length < 10)
        {
            SetError("Alasan mutasi minimal 10 karakter");
            return;
        }

        if (TanggalMutasi > DateTime.Today)
        {
            SetError("Tanggal mutasi tidak boleh di masa depan");
            return;
        }

        await ExecuteAsync(async () =>
        {
            var request = new MutationCreateRequest
            {
                AsetId = SelectedAsset.Id,
                RuanganTujuanId = SelectedRuanganTujuan.Id,
                Alasan = Alasan.Trim(),
                TanggalMutasi = TanggalMutasi,
                KondisiSaatMutasi = SelectedKondisi
            };

            var response = await _apiService.CreateMutationAsync(request);
            if (response.Success)
            {
                Log.Information("Mutation created: {MutationId}", response.Data?.Id);
                DialogService.ShowSnackbar("Mutasi berhasil dibuat");
                HideForm();
                await LoadDataAsync();
            }
        });
    }

    [RelayCommand]
    private async Task CompleteMutationAsync(Mutation? mutation)
    {
        if (!CanManage)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk menyelesaikan mutasi");
            return;
        }

        if (mutation == null) return;

        var confirm = await DialogService.ShowConfirmAsync(
            "Konfirmasi",
            $"Apakah Anda yakin ingin menyelesaikan mutasi aset '{mutation.NamaAset}'?");

        if (!confirm) return;

        await ExecuteAsync(async () =>
        {
            var response = await _apiService.CompleteMutationAsync(mutation.Id);
            if (response.Success)
            {
                Log.Information("Mutation completed: {MutationId}", mutation.Id);
                DialogService.ShowSnackbar("Mutasi berhasil diselesaikan");
                await LoadDataAsync();
            }
        });
    }

    [RelayCommand]
    private async Task CancelMutationAsync(Mutation? mutation)
    {
        if (!CanManage)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk membatalkan mutasi");
            return;
        }

        if (mutation == null) return;

        var reason = await DialogService.ShowInputAsync(
            "Batalkan Mutasi",
            $"Masukkan alasan pembatalan mutasi aset '{mutation.NamaAset}':\n(minimal 10 karakter)");

        if (string.IsNullOrWhiteSpace(reason)) return;

        if (reason.Length < 10)
        {
            await DialogService.ShowWarningAsync("Validasi", "Alasan pembatalan minimal 10 karakter");
            return;
        }

        await ExecuteAsync(async () =>
        {
            var response = await _apiService.CancelMutationAsync(mutation.Id, new MutationCancelRequest { AlasanPembatalan = reason });
            if (response.Success)
            {
                Log.Information("Mutation cancelled: {MutationId}", mutation.Id);
                DialogService.ShowSnackbar("Mutasi berhasil dibatalkan");
                await LoadDataAsync();
            }
        });
    }

    [RelayCommand]
    private async Task NextPageAsync()
    {
        if (CurrentPage < TotalPages)
        {
            CurrentPage++;
            await LoadMutationsAsync();
        }
    }

    [RelayCommand]
    private async Task PreviousPageAsync()
    {
        if (CurrentPage > 1)
        {
            CurrentPage--;
            await LoadMutationsAsync();
        }
    }

    partial void OnSelectedStatusChanged(string? value)
    {
        CurrentPage = 1;
        OnPropertyChanged(nameof(ShowAll));
        OnPropertyChanged(nameof(ShowPending));
        OnPropertyChanged(nameof(ShowCompleted));
        OnPropertyChanged(nameof(ShowCancelled));
    }

    partial void OnSelectedMutationChanged(Mutation? value)
    {
        OnPropertyChanged(nameof(HasSelection));
        OnPropertyChanged(nameof(HasNoSelection));
        OnPropertyChanged(nameof(CanModify));
        OnPropertyChanged(nameof(CanComplete));
        OnPropertyChanged(nameof(CanCancel));
    }

    [RelayCommand]
    private async Task FilterAsync(string status)
    {
        SelectedStatus = status;
        await LoadMutationsAsync();
    }

    [RelayCommand]
    private async Task CompleteSelectedMutationAsync()
    {
        if (SelectedMutation == null) return;
        await CompleteMutationAsync(SelectedMutation);
    }

    [RelayCommand]
    private async Task CancelSelectedMutationAsync()
    {
        if (SelectedMutation == null) return;
        await CancelMutationAsync(SelectedMutation);
    }

    [RelayCommand]
    private void ShowCreateMutationForm()
    {
        ShowCreateForm();
    }
}
