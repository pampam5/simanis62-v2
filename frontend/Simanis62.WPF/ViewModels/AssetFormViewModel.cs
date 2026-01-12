using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Serilog;
using Simanis62.Models;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels.Base;

namespace Simanis62.ViewModels;

/// <summary>
/// ViewModel untuk form aset (create/edit).
/// </summary>
public partial class AssetFormViewModel : ViewModelBase
{
    private readonly IApiService _apiService;
    private Asset? _editingAsset;

    [ObservableProperty]
    private bool _isEditMode;

    [ObservableProperty]
    private string _pageTitle = "Tambah Aset Baru";

    // Common fields
    [ObservableProperty]
    private string _kodeBarang = string.Empty;

    [ObservableProperty]
    private string _namaBarang = string.Empty;

    [ObservableProperty]
    private string _selectedKategori = "B";

    [ObservableProperty]
    private string _selectedKondisi = "Baik";

    [ObservableProperty]
    private string _hargaText = string.Empty;

    [ObservableProperty]
    private int _tahunPerolehan = DateTime.Now.Year;

    [ObservableProperty]
    private string? _asalPerolehan;

    [ObservableProperty]
    private string? _keterangan;

    [ObservableProperty]
    private Room? _selectedRuangan;

    // KIB B specific fields
    [ObservableProperty]
    private string? _merk;

    [ObservableProperty]
    private string? _tipe;

    [ObservableProperty]
    private string? _ukuranCc;

    [ObservableProperty]
    private string _selectedSatuan = "Unit";

    [ObservableProperty]
    private string? _nomorRangka;

    [ObservableProperty]
    private string? _nomorMesin;

    [ObservableProperty]
    private string? _nomorPolisi;

    [ObservableProperty]
    private string? _nomorBpkb;

    [ObservableProperty]
    private string? _bahan;

    [ObservableProperty]
    private string? _nomorPabrik;

    [ObservableProperty]
    private string? _nomorBast;

    [ObservableProperty]
    private string? _asalUsul;

    [ObservableProperty]
    private ObservableCollection<Room> _rooms = new();

    public bool CanSave => SessionService.IsAdmin;
    public bool CanEdit => SessionService.IsAdmin;
    public bool IsKibB => SelectedKategori == "B";
    public bool IsNewAsset => !IsEditMode;
    public string SaveButtonText => IsEditMode ? "Simpan Perubahan" : "Simpan";

    public List<string> KategoriOptions { get; } = new() { "A", "B", "C", "D", "E", "F" };
    public List<string> KondisiOptions { get; } = new() { "Baik", "Rusak_Ringan", "Rusak_Berat" };
    public List<string> SatuanOptions { get; } = new() { "Unit", "Buah", "Set", "Paket", "Lembar", "Rim", "Dus", "Lusin" };
    public List<string> AsalUsulOptions { get; } = new() { "Pembelian", "Hibah", "Sumbangan", "Tukar Menukar", "Lainnya" };

    public AssetFormViewModel(
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

        // Check if editing existing asset
        var asset = NavigationService.GetParameter<Asset>();
        if (asset != null)
        {
            _editingAsset = asset;
            IsEditMode = true;
            PageTitle = "Edit Aset";
            LoadAssetData(asset);
        }
    }

    private async Task LoadRoomsAsync()
    {
        var response = await _apiService.GetRoomsAsync(1, 1000);
        if (response.Success)
        {
            Rooms = new ObservableCollection<Room>(response.Data);
        }
    }

    private void LoadAssetData(Asset asset)
    {
        KodeBarang = asset.KodeBarang;
        NamaBarang = asset.NamaBarang;
        SelectedKategori = asset.KategoriKib;
        SelectedKondisi = asset.Kondisi;
        HargaText = asset.Harga.ToString();
        TahunPerolehan = asset.TahunPerolehan;
        AsalPerolehan = asset.AsalPerolehan;
        Keterangan = asset.Keterangan;
        SelectedRuangan = Rooms.FirstOrDefault(r => r.Id == asset.RuanganId);

        // KIB B fields
        Merk = asset.Merk;
        Tipe = asset.Tipe;
        UkuranCc = asset.UkuranCc;
        SelectedSatuan = asset.Satuan ?? "Unit";
        NomorRangka = asset.NomorRangka;
        NomorMesin = asset.NomorMesin;
        NomorPolisi = asset.NomorPolisi;
        NomorBpkb = asset.NomorBpkb;
        Bahan = asset.Bahan;
    }

    [RelayCommand]
    private async Task SaveAsync()
    {
        if (!CanSave)
        {
            DialogService.ShowSnackbar("Anda tidak memiliki izin untuk menyimpan aset");
            return;
        }

        // Validate
        if (!ValidateForm()) return;

        await ExecuteAsync(async () =>
        {
            var request = new AssetRequest
            {
                KodeBarang = KodeBarang.Trim(),
                NamaBarang = NamaBarang.Trim(),
                KategoriKib = SelectedKategori,
                Kondisi = SelectedKondisi,
                Harga = long.Parse(HargaText.Replace(".", "").Replace(",", "")),
                TahunPerolehan = TahunPerolehan,
                AsalPerolehan = AsalPerolehan?.Trim(),
                Keterangan = Keterangan?.Trim(),
                RuanganId = SelectedRuangan?.Id,
                Merk = Merk?.Trim(),
                Tipe = Tipe?.Trim(),
                UkuranCc = UkuranCc?.Trim(),
                Satuan = SelectedSatuan,
                NomorRangka = NomorRangka?.Trim(),
                NomorMesin = NomorMesin?.Trim(),
                NomorPolisi = NomorPolisi?.Trim(),
                NomorBpkb = NomorBpkb?.Trim(),
                Bahan = Bahan?.Trim()
            };

            if (IsEditMode && _editingAsset != null)
            {
                var response = await _apiService.UpdateAssetAsync(_editingAsset.Id, request);
                if (response.Success)
                {
                    Log.Information("Asset updated: {AssetId}", _editingAsset.Id);
                    DialogService.ShowSnackbar("Aset berhasil diperbarui");
                    NavigationService.GoBack();
                }
            }
            else
            {
                var response = await _apiService.CreateAssetAsync(request);
                if (response.Success)
                {
                    Log.Information("Asset created: {AssetId}", response.Data?.Id);
                    DialogService.ShowSnackbar("Aset berhasil ditambahkan");
                    NavigationService.GoBack();
                }
            }
        });
    }

    private bool ValidateForm()
    {
        ClearError();

        if (string.IsNullOrWhiteSpace(KodeBarang))
        {
            SetError("Kode barang harus diisi");
            return false;
        }

        // Validate kode barang format: XX.XX.XX.XXXX
        if (!System.Text.RegularExpressions.Regex.IsMatch(KodeBarang, @"^\d{2}\.\d{2}\.\d{2}\.\d{4}$"))
        {
            SetError("Format kode barang tidak valid. Gunakan format: XX.XX.XX.XXXX");
            return false;
        }

        if (string.IsNullOrWhiteSpace(NamaBarang))
        {
            SetError("Nama barang harus diisi");
            return false;
        }

        if (NamaBarang.Length < 3 || NamaBarang.Length > 200)
        {
            SetError("Nama barang harus 3-200 karakter");
            return false;
        }

        if (string.IsNullOrWhiteSpace(HargaText) || !long.TryParse(HargaText.Replace(".", "").Replace(",", ""), out var harga))
        {
            SetError("Harga harus berupa angka");
            return false;
        }

        if (harga <= 0 || harga > 999_999_999_999)
        {
            SetError("Harga harus lebih dari 0 dan maksimal 999.999.999.999");
            return false;
        }

        if (TahunPerolehan < 1900 || TahunPerolehan > DateTime.Now.Year)
        {
            SetError($"Tahun perolehan harus antara 1900 - {DateTime.Now.Year}");
            return false;
        }

        return true;
    }

    [RelayCommand]
    private void Cancel()
    {
        NavigationService.GoBack();
    }

    [RelayCommand]
    private void GoBack()
    {
        NavigationService.GoBack();
    }

    partial void OnSelectedKategoriChanged(string value)
    {
        OnPropertyChanged(nameof(IsKibB));
    }
}
