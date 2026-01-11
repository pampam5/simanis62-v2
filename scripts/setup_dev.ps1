# Setup Development Environment
Write-Host 'Setting up Backend...'
pip install -r ..\backend\requirements.txt
Write-Host 'Setting up Frontend...'
dotnet restore ..\frontend\Simanis62.WPF\Simanis62.WPF.csproj
