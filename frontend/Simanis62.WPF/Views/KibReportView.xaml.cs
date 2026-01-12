using System.Windows;
using System.Windows.Controls;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.ViewModels;

namespace Simanis62.Views;

/// <summary>
/// Code-behind untuk KibReportView.
/// </summary>
public partial class KibReportView : UserControl
{
    public KibReportView()
    {
        InitializeComponent();
        DataContext = App.Services.GetRequiredService<KibReportViewModel>();
    }

    private async void OnLoaded(object sender, RoutedEventArgs e)
    {
        if (DataContext is KibReportViewModel vm)
        {
            await vm.OnLoadedAsync();
        }
    }
}
