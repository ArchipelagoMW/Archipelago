#define sourcepath "build_factorio\exe.win-amd64-3.8\"
#define MyAppName "Archipelago Factorio Client"
#define MyAppExeName "ArchipelagoGraphicalFactorioClient.exe"
#define MyAppIcon "data/icon.ico"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{D13CEBD0-F1D5-4435-A4A6-5243F934613F}}
AppName={#MyAppName}
AppVerName={#MyAppName}
DefaultDirName={commonappdata}\{#MyAppName}
DisableProgramGroupPage=yes
DefaultGroupName=Archipelago
OutputDir=setups
OutputBaseFilename=Setup {#MyAppName}
Compression=lzma2
SolidCompression=yes
LZMANumBlockThreads=8
ArchitecturesInstallIn64BitMode=x64
ChangesAssociations=yes
ArchitecturesAllowed=x64
AllowNoIcons=yes
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}
SignTool= signtool
LicenseFile= LICENSE
WizardStyle= modern
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";


[Dirs]
NAME: "{app}"; Flags: setntfscompression; Permissions: everyone-modify users-modify authusers-modify;

[Files]
Source: "vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall
Source: "{#sourcepath}*"; Excludes: "*.sfc, *.log, data\sprites\alttpr"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName} Folder"; Filename: "{app}";
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}";
Name: "{commondesktop}\{#MyAppName} Folder"; Filename: "{app}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/passive /norestart"; Check: IsVCRedist64BitNeeded; StatusMsg: "Installing VC++ redistributable..."

[UninstallDelete]
Type: dirifempty; Name: "{app}"


[Code]
// See: https://stackoverflow.com/a/51614652/2287576
function IsVCRedist64BitNeeded(): boolean;
var
  strVersion: string;
begin
  if (RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Version', strVersion)) then
  begin
    // Is the installed version at least the packaged one ?
    Log('VC Redist x64 Version : found ' + strVersion);
    Result := (CompareStr(strVersion, 'v14.29.30037') < 0);
  end
  else
  begin
    // Not even an old version installed
    Log('VC Redist x64 is not already installed');
    Result := True;
  end;
end;


