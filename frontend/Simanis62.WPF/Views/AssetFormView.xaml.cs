using System.Windows;
using System.Windows.Controls;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.ViewModels;

namespace Simanis62.Views;

/// <summary>
/// Code-behind untuk AssetFormView.
/// </summary>
public partial class AssetFormView : UserControl
{
    public AssetFormView()
    {
        InitializeComponent();
        DataContext = App.Services.GetRequiredService<AssetFormViewModel>();
    }

    private async void OnLoaded(object sender, RoutedEventArgs e)
    {
        if (DataContext is AssetFormViewModel vm)
        {
            await vm.OnLoadedAsync();
        }
    }
}
