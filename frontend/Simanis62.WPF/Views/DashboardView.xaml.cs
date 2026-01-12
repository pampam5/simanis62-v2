using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.ViewModels;

namespace Simanis62.Views;

/// <summary>
/// Code-behind untuk DashboardView.
/// </summary>
public partial class DashboardView : UserControl
{
    public DashboardView()
    {
        InitializeComponent();
        DataContext = App.Services.GetRequiredService<DashboardViewModel>();
    }

    private async void OnLoaded(object sender, RoutedEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            await vm.OnLoadedAsync();
        }
    }

    private void OnAssetCardClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToAssetsCommand.Execute(null);
        }
    }

    private void OnMutationCardClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToMutationsCommand.Execute(null);
        }
    }

    private void OnKibAClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToKibReportCommand.Execute("A");
        }
    }

    private void OnKibBClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToKibReportCommand.Execute("B");
        }
    }

    private void OnKibCClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToKibReportCommand.Execute("C");
        }
    }

    private void OnKibDClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToKibReportCommand.Execute("D");
        }
    }

    private void OnKibEClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToKibReportCommand.Execute("E");
        }
    }

    private void OnKibFClick(object sender, MouseButtonEventArgs e)
    {
        if (DataContext is DashboardViewModel vm)
        {
            vm.NavigateToKibReportCommand.Execute("F");
        }
    }
}
