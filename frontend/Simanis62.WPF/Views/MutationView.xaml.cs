using System.Windows;
using System.Windows.Controls;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.ViewModels;

namespace Simanis62.Views;

/// <summary>
/// Code-behind untuk MutationView.
/// </summary>
public partial class MutationView : UserControl
{
    public MutationView()
    {
        InitializeComponent();
        DataContext = App.Services.GetRequiredService<MutationViewModel>();
    }

    private async void OnLoaded(object sender, RoutedEventArgs e)
    {
        if (DataContext is MutationViewModel vm)
        {
            await vm.OnLoadedAsync();
        }
    }
}
