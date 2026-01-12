using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace Simanis62.Converters;

/// <summary>
/// Converts boolean to Visibility (true = Visible, false = Collapsed).
/// </summary>
public class BoolToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is bool boolValue)
        {
            // If parameter is "Inverse", invert the logic
            if (parameter?.ToString() == "Inverse")
            {
                return boolValue ? Visibility.Collapsed : Visibility.Visible;
            }
            return boolValue ? Visibility.Visible : Visibility.Collapsed;
        }
        return Visibility.Collapsed;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is Visibility visibility)
        {
            return visibility == Visibility.Visible;
        }
        return false;
    }
}

/// <summary>
/// Converts null to Visibility (null = Collapsed, not null = Visible).
/// </summary>
public class NullToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        var isNull = value == null;
        if (parameter?.ToString() == "Inverse")
        {
            return isNull ? Visibility.Visible : Visibility.Collapsed;
        }
        return isNull ? Visibility.Collapsed : Visibility.Visible;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

/// <summary>
/// Converts string to Visibility (empty = Collapsed, not empty = Visible).
/// </summary>
public class StringToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        var isEmpty = string.IsNullOrWhiteSpace(value?.ToString());
        if (parameter?.ToString() == "Inverse")
        {
            return isEmpty ? Visibility.Visible : Visibility.Collapsed;
        }
        return isEmpty ? Visibility.Collapsed : Visibility.Visible;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

/// <summary>
/// Converts role to Visibility for Admin-only elements.
/// </summary>
public class AdminVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is string role)
        {
            return role == "Admin" ? Visibility.Visible : Visibility.Collapsed;
        }
        return Visibility.Collapsed;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

/// <summary>
/// Converts currency value to formatted string.
/// </summary>
public class CurrencyConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is long longValue)
        {
            return $"Rp {longValue:N0}";
        }
        if (value is int intValue)
        {
            return $"Rp {intValue:N0}";
        }
        if (value is decimal decimalValue)
        {
            return $"Rp {decimalValue:N0}";
        }
        return "Rp 0";
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is string strValue)
        {
            var cleanValue = strValue.Replace("Rp", "").Replace(".", "").Replace(",", "").Trim();
            if (long.TryParse(cleanValue, out var result))
            {
                return result;
            }
        }
        return 0L;
    }
}

/// <summary>
/// Converts status to color.
/// </summary>
public class StatusToColorConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        var status = value?.ToString() ?? "";
        return status switch
        {
            "Aktif" => "#388E3C",      // Green
            "Baik" => "#388E3C",       // Green
            "Selesai" => "#388E3C",    // Green
            "Rusak" => "#D32F2F",      // Red
            "Rusak_Ringan" => "#F57C00", // Orange
            "Rusak_Berat" => "#D32F2F", // Red
            "Dihapus" => "#757575",    // Gray
            "Dibatalkan" => "#757575", // Gray
            "Mutasi" => "#1565C0",     // Blue
            "Dalam_Proses" => "#F57C00", // Orange
            "Baru" => "#00897B",       // Teal
            _ => "#757575"             // Gray
        };
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

/// <summary>
/// Converts status to display text.
/// </summary>
public class StatusDisplayConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        var status = value?.ToString() ?? "";
        return status switch
        {
            "Dalam_Proses" => "Dalam Proses",
            "Rusak_Ringan" => "Rusak Ringan",
            "Rusak_Berat" => "Rusak Berat",
            _ => status
        };
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

/// <summary>
/// Converts date to formatted string.
/// </summary>
public class DateFormatConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is DateTime dateTime)
        {
            var format = parameter?.ToString() ?? "dd/MM/yyyy";
            return dateTime.ToString(format);
        }
        return "-";
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is string strValue && DateTime.TryParse(strValue, out var result))
        {
            return result;
        }
        return DateTime.MinValue;
    }
}

/// <summary>
/// Inverse boolean to Visibility converter.
/// </summary>
public class InverseBoolToVisibilityConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is bool boolValue)
        {
            return boolValue ? Visibility.Collapsed : Visibility.Visible;
        }
        return Visibility.Visible;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is Visibility visibility)
        {
            return visibility != Visibility.Visible;
        }
        return true;
    }
}

/// <summary>
/// Converts integer > 1 to true for pagination.
/// </summary>
public class GreaterThanOneConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is int intValue)
        {
            return intValue > 1;
        }
        return false;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}
