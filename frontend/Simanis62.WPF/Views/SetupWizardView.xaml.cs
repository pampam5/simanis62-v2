using System.Windows.Controls;
using Microsoft.Extensions.DependencyInjection;
using Simanis62.ViewModels;

namespace Simanis62.Views;

/// <summary>
/// Code-behind untuk SetupWizardView.
/// </summary>
public partial class SetupWizardView : UserControl
{
    public SetupWizardView()
    {
        InitializeComponent();
        DataContext = App.Services.GetRequiredService<SetupWizardViewModel>();
    }
}
