; SIMANIS62 Installer Script
; Inno Setup 6.x
; 
; Author: SIMANIS62 Team
; Version: 1.0
; Date: 2026-01-12

#ifndef AppVersion
  #define AppVersion "2.0.0"
#endif

#define AppName "SIMANIS62"
#define AppPublisher "SIMANIS62 Team"
#define AppURL "https://github.com/simanis62"
#define AppExeName "Simanis62.exe"
#define AppId "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
; Output settings
OutputDir=Output
OutputBaseFilename=Simanis62_Setup_v{#AppVersion}
; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
; UI settings
WizardStyle=modern
; SetupIconFile=..\frontend\Simanis62.WPF\Resources\app.ico
; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; Uninstall
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Frontend (WPF Application)
Source: "..\dist\Simanis62.WPF\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Backend (FastAPI Server) - dalam subfolder
Source: "..\dist\Simanis62.API\*"; DestDir: "{app}\API"; Flags: ignoreversion recursesubdirs createallsubdirs

; Configuration files
Source: "..\configs\production.json"; DestDir: "{commonappdata}\Simanis62"; DestName: "config.json"; Flags: onlyifdoesntexist

; Distribution files
Source: "distribution\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "distribution\LISENSI.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; Create data directories
Name: "{commonappdata}\Simanis62"; Permissions: users-modify
Name: "{commonappdata}\Simanis62\backups"; Permissions: users-modify
Name: "{commonappdata}\Simanis62\logs"; Permissions: users-modify

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to run after install
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up logs on uninstall (keep database for safety)
Type: filesandordirs; Name: "{commonappdata}\Simanis62\logs"

[Code]
// Pascal Script untuk custom logic

var
  DotNetPage: TOutputMsgWizardPage;
  NeedsDotNet: Boolean;

// Check if .NET 8 Desktop Runtime is installed
function IsDotNet8DesktopInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  // Check using dotnet --list-runtimes
  Result := Exec('dotnet', '--list-runtimes', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  if Result then
  begin
    // Simple check - if dotnet command works, assume runtime is available
    // For production, use more robust check with registry or netcorecheck.exe
    Result := (ResultCode = 0);
  end;
end;

// Check .NET on initialization
procedure InitializeWizard();
begin
  NeedsDotNet := not IsDotNet8DesktopInstalled();
  
  if NeedsDotNet then
  begin
    DotNetPage := CreateOutputMsgPage(wpWelcome,
      '.NET 8 Desktop Runtime Diperlukan',
      'Aplikasi ini memerlukan .NET 8 Desktop Runtime',
      'SIMANIS62 memerlukan .NET 8 Desktop Runtime untuk berjalan.' + #13#10 + #13#10 +
      'Setelah instalasi selesai, silakan download dan install .NET 8 Desktop Runtime dari:' + #13#10 +
      'https://dotnet.microsoft.com/download/dotnet/8.0' + #13#10 + #13#10 +
      'Pilih "Download .NET Desktop Runtime" untuk Windows x64.');
  end;
end;

// Create appsettings.json for frontend
procedure CreateAppSettings();
var
  AppSettingsPath: String;
  Content: String;
begin
  AppSettingsPath := ExpandConstant('{app}\appsettings.json');
  
  if not FileExists(AppSettingsPath) then
  begin
    Content := '{' + #13#10 +
      '  "AppSettings": {' + #13#10 +
      '    "ApiBaseUrl": "http://127.0.0.1:8000",' + #13#10 +
      '    "AppName": "SIMANIS62",' + #13#10 +
      '    "Version": "' + '{#AppVersion}' + '",' + #13#10 +
      '    "Environment": "Production",' + #13#10 +
      '    "LogLevel": "Information",' + #13#10 +
      '    "GlitchTipDsn": ""' + #13#10 +
      '  }' + #13#10 +
      '}';
    SaveStringToFile(AppSettingsPath, Content, False);
  end;
end;

// Post-install actions
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    CreateAppSettings();
  end;
end;
