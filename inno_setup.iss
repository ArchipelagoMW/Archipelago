#define sourcepath "build\exe.win-amd64-3.8\"
#define MyAppName "BerserkerMultiWorld"
#define MyAppExeName "BerserkerMultiClient.exe"
#define MyAppIcon "icon.ico"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{6D826EE0-49BE-4B36-BACE-09C6971CD85C}}
AppName={#MyAppName}
AppVerName={#MyAppName}
DefaultDirName={commonappdata}\{#MyAppName}
DisableProgramGroupPage=yes
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
Source: "{code:GetROMPath}"; DestDir: "{app}"; DestName: "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"; Flags: external
Source: "{#sourcepath}*"; Excludes: "*.key, *.log, *.hpkey"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName} Folder"; Filename: "{app}";
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}";
Name: "{commondesktop}\{#MyAppName} Folder"; Filename: "{app}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/passive /norestart"; Check: IsVCRedist64BitNeeded; StatusMsg: "Installing VC++ redistributable..."
; Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Registry]

Root: HKCR; Subkey: ".bmbp";                                 ValueData: "{#MyAppName}patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: ""
Root: HKCR; Subkey: "{#MyAppName}patch";                     ValueData: "{#MyAppName} Patch";       Flags: uninsdeletekey;   ValueType: string;  ValueName: ""
Root: HKCR; Subkey: "{#MyAppName}patch\DefaultIcon";         ValueData: "{app}\{#MyAppExeName},0";                           ValueType: string;  ValueName: ""
Root: HKCR; Subkey: "{#MyAppName}patch\shell\open\command";  ValueData: """{app}\{#MyAppExeName}"" ""%1""";                  ValueType: string;  ValueName: ""



[Code]
// See: https://stackoverflow.com/a/51614652/2287576
function IsVCRedist64BitNeeded(): boolean;
var
  strVersion: string;
begin
  if (RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Version', strVersion)) then
  begin
    // Is the installed version at least 14.24 ? 
    Log('VC Redist x64 Version : found ' + strVersion);
    Result := (CompareStr(strVersion, 'v14.24.28127.4') < 0);
  end
  else
  begin
    // Not even an old version installed
    Log('VC Redist x64 is not already installed');
    Result := True;
  end;
end;

var ROMFilePage: TInputFileWizardPage;
var R : longint;

procedure InitializeWizard();
begin
  ROMFilePage :=
    CreateInputFilePage(
      wpLicense,
      'Select ROM File',
      'Where is your Zelda no Densetsu - Kamigami no Triforce (Japan).sfc located?',
      'Select the file, then click Next.');

  ROMFilePage.Add(
    'Location of ROM file:',         
    'SNES ROM files|*.sfc|All files|*.*', 
    '.sfc');                             
end;

function GetROMPath(Param: string): string;
begin
  if Assigned(RomFilePage) then    begin
      R := CompareStr(GetMD5OfFile(ROMFilePage.Values[0]), '03a63945398191337e896e5771f77173')
      if R <> 0 then
        MsgBox('ROM validation failed. Very likely wrong file.', mbInformation, MB_OK);  
      Result := ROMFilePage.Values[0]
    end
  else
    Result := '';
 end;
