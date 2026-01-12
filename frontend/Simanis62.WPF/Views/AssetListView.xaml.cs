using System.Windows;
using System.Windows.Controls;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.ViewModels;

namespace Simanis62.Views;

/// <summary>
/// Code-behind untuk AssetListView.
/// </summary>
public partial class AssetListView : UserControl
{
    public AssetListView()
    {
        InitializeComponent();
        DataContext = App.Services.GetRequiredService<AssetListViewModel>();
    }

    private async void OnLoaded(object sender, RoutedEventArgs e)
    {
        if (DataContext is AssetListViewModel vm)
        {
            await vm.OnLoadedAsync();
        }
    }
}
