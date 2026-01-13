using System.Windows;
using System.Windows.Controls;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.Services.Interfaces;
using Simanis62.ViewModels;
using Simanis62.Views;

namespace Simanis62;

/// <summary>
/// MainWindow - Shell utama aplikasi SIMANIS62.
/// </summary>
public partial class MainWindow : Window
{
    private readonly INavigationService _navigationService;
    private readonly MainViewModel _viewModel;

    public MainWindow()
    {
        InitializeComponent();

        _viewModel = App.Services.GetRequiredService<MainViewModel>();
        _navigationService = App.Services.GetRequiredService<INavigationService>();

        DataContext = _viewModel;

        // Setup navigation
        _navigationService.NavigationChanged += OnNavigationChanged;
    }

    private void OnNavigationChanged(string viewName)
    {
        UserControl? view = viewName switch
        {
            "Login" => App.Services.GetRequiredService<LoginView>(),
            "Dashboard" => App.Services.GetRequiredService<DashboardView>(),
            "AssetList" => App.Services.GetRequiredService<AssetListView>(),
            "AssetForm" => App.Services.GetRequiredService<AssetFormView>(),
            "KibReport" => App.Services.GetRequiredService<KibReportView>(),
            "Mutation" => App.Services.GetRequiredService<MutationView>(),
            "SetupWizard" => App.Services.GetRequiredService<SetupWizardView>(),
            _ => App.Services.GetRequiredService<DashboardView>()
        };

        ContentFrame.Content = view;
    }
}
