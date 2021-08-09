#define sourcepath "build\exe.win-amd64-3.8"
#define MyAppName "Archipelago"
#define MyAppExeName "ArchipelagoServer.exe"
#define MyAppIcon "data/icon.ico"
#dim VersionTuple[4]
#define MyAppVersion ParseVersion('build\exe.win-amd64-3.8\ArchipelagoServer.exe', VersionTuple[0], VersionTuple[1], VersionTuple[2], VersionTuple[3])
#define MyAppVersionText Str(VersionTuple[0])+"."+Str(VersionTuple[1])+"."+Str(VersionTuple[2])


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{918BA46A-FAB8-460C-9DFF-AE691E1C865B}}
AppName={#MyAppName}
AppCopyright=Distributed under MIT License
AppVerName={#MyAppName} {#MyAppVersionText}
VersionInfoVersion={#MyAppVersion}
DefaultDirName={commonappdata}\{#MyAppName}
DisableProgramGroupPage=yes
DefaultGroupName=Archipelago
OutputDir=setups
OutputBaseFilename=Setup {#MyAppName} {#MyAppVersionText}
Compression=lzma2
SolidCompression=yes
LZMANumBlockThreads=8
ArchitecturesInstallIn64BitMode=x64
ChangesAssociations=yes
ArchitecturesAllowed=x64
AllowNoIcons=yes
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}
; you will likely have to remove the following signtool line when testing/debugging localy. Don't include that change in PRs.
SignTool= signtool
LicenseFile= LICENSE
WizardStyle= modern
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

[Types]
Name: "full"; Description: "Full installation"
Name: "hosting"; Description: "Installation for hosting purposes"
Name: "playing"; Description: "Installation for playing purposes"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "core"; Description: "Core Files"; Types: full hosting playing custom; Flags: fixed
Name: "generator"; Description: "Generator"; Types: full hosting
Name: "server"; Description: "Server"; Types: full hosting
Name: "client"; Description: "Clients"; Types: full playing
Name: "client/lttp"; Description: "A Link to the Past"; Types: full playing hosting
Name: "client/factorio"; Description: "Factorio"; Types: full playing
Name: "client/minecraft"; Description: "Minecraft"; Types: full playing; ExtraDiskSpaceRequired: 226894278

[Dirs]
NAME: "{app}"; Flags: setntfscompression; Permissions: everyone-modify users-modify authusers-modify;

[Files]
Source: "{code:GetROMPath}"; DestDir: "{app}"; DestName: "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"; Flags: external; Components: client/lttp or generator
Source: "{#sourcepath}\*"; Excludes: "*.sfc, *.log, data\sprites\alttpr, SNI, EnemizerCLI, *exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#sourcepath}\SNI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\SNI"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: client/lttp
Source: "{#sourcepath}\EnemizerCLI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\EnemizerCLI"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: generator

Source: "{#sourcepath}\ArchipelagoGenerate.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: generator
Source: "{#sourcepath}\ArchipelagoServer.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: server
Source: "{#sourcepath}\ArchipelagoFactorioClient.exe";  DestDir: "{app}"; Flags: ignoreversion; Components: client/factorio
Source: "{#sourcepath}\ArchipelagoLttPClient.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/lttp
Source: "{#sourcepath}\ArchipelagoLttPAdjuster.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/lttp
Source: "{#sourcepath}\ArchipelagoMinecraftClient.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/minecraft
Source: "vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall

;minecraft temp files
Source: "{tmp}\forge-installer.jar"; DestDir: "{app}"; Flags: skipifsourcedoesntexist external deleteafterinstall; Components: client/minecraft

[Icons]
Name: "{group}\{#MyAppName} Folder"; Filename: "{app}";
Name: "{group}\{#MyAppName} Server"; Filename: "{app}\{#MyAppExeName}"; Components: server
Name: "{group}\{#MyAppName} LttP Client"; Filename: "{app}\ArchipelagoLttPClient.exe"; Components: client/lttp
Name: "{group}\{#MyAppName} Factorio Client"; Filename: "{app}\ArchipelagoFactorioClient.exe"; Components: client/factorio
Name: "{group}\{#MyAppName} Minecraft Client"; Filename: "{app}\ArchipelagoMinecraftClient.exe"; Components: client/minecraft
Name: "{commondesktop}\{#MyAppName} Folder"; Filename: "{app}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName} Server"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Components: server
Name: "{commondesktop}\{#MyAppName} LttP Client"; Filename: "{app}\ArchipelagoLttPClient.exe"; Tasks: desktopicon; Components: client/lttp
Name: "{commondesktop}\{#MyAppName} Factorio Client"; Filename: "{app}\ArchipelagoFactorioClient.exe"; Tasks: desktopicon; Components: client/factorio

[Run]

Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/passive /norestart"; Check: IsVCRedist64BitNeeded; StatusMsg: "Installing VC++ redistributable..."
Filename: "{app}\ArchipelagoLttPAdjuster"; Parameters: "--update_sprites"; StatusMsg: "Updating Sprite Library..."; Components: client/lttp or generator
Filename: "{app}\jre8\bin\java.exe"; Parameters: "-jar ""{app}\forge-installer.jar"" --installServer ""{app}\Minecraft Forge server"""; Flags: runhidden; Check: IsForgeNeeded(); StatusMsg: "Installing Forge Server..."; Components: client/minecraft

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Registry]

Root: HKCR; Subkey: ".apbp";                                 ValueData: "{#MyAppName}patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Components: client/lttp
Root: HKCR; Subkey: "{#MyAppName}patch";                     ValueData: "Archipelago Binary Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: ""; Components: client/lttp
Root: HKCR; Subkey: "{#MyAppName}patch\DefaultIcon";         ValueData: "{app}\ArchipelagoLttPClient.exe,0";                           ValueType: string;  ValueName: ""; Components: client/lttp
Root: HKCR; Subkey: "{#MyAppName}patch\shell\open\command";  ValueData: """{app}\ArchipelagoLttPClient.exe"" ""%1""";                  ValueType: string;  ValueName: ""; Components: client/lttp

Root: HKCR; Subkey: ".apmc";                                  ValueData: "{#MyAppName}mcdata";         Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Components: client/minecraft
Root: HKCR; Subkey: "{#MyAppName}mcdata";                     ValueData: "Archipelago Minecraft Data"; Flags: uninsdeletekey;   ValueType: string;  ValueName: ""; Components: client/minecraft
Root: HKCR; Subkey: "{#MyAppName}mcdata\DefaultIcon";         ValueData: "{app}\ArchipelagoMinecraftClient.exe,0";                           ValueType: string;  ValueName: ""; Components: client/minecraft
Root: HKCR; Subkey: "{#MyAppName}mcdata\shell\open\command";  ValueData: """{app}\ArchipelagoMinecraftClient.exe"" ""%1""";                  ValueType: string;  ValueName: ""; Components: client/minecraft

Root: HKCR; Subkey: ".archipelago";                              ValueData: "{#MyAppName}multidata";        Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Components: server
Root: HKCR; Subkey: "{#MyAppName}multidata";                     ValueData: "Archipelago Server Data";       Flags: uninsdeletekey;  ValueType: string;  ValueName: ""; Components: server
Root: HKCR; Subkey: "{#MyAppName}multidata\DefaultIcon";         ValueData: "{app}\ArchipelagoServer.exe,0";                         ValueType: string;  ValueName: ""; Components: server
Root: HKCR; Subkey: "{#MyAppName}multidata\shell\open\command";  ValueData: """{app}\ArchipelagoServer.exe"" ""%1""";                ValueType: string;  ValueName: ""; Components: server



[Code]
const
  SHCONTCH_NOPROGRESSBOX = 4;
  SHCONTCH_RESPONDYESTOALL = 16;
  FORGE_VERSION = '1.16.5-36.2.0';

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

function IsForgeNeeded(): boolean;
begin
  Result := True;
  if (FileExists(ExpandConstant('{app}')+'\Minecraft Forge Server\forge-'+FORGE_VERSION+'.jar')) then
    Result := False;
end;

function IsJavaNeeded(): boolean;
begin
  Result := True;
  if (FileExists(ExpandConstant('{app}')+'\jre8\bin\java.exe')) then
    Result := False;
end;

function OnDownloadMinecraftProgress(const Url, FileName: String; const Progress, ProgressMax: Int64): Boolean;
begin
  if Progress = ProgressMax then
    Log(Format('Successfully downloaded Minecraft additional files to {tmp}: %s', [FileName]));
  Result := True;
end;

procedure UnZip(ZipPath, TargetPath: string);
var
  Shell: Variant;
  ZipFile: Variant;
  TargetFolder: Variant;
begin
  Shell := CreateOleObject('Shell.Application');

  ZipFile := Shell.NameSpace(ZipPath);
  if VarIsClear(ZipFile) then
    RaiseException(
      Format('ZIP file "%s" does not exist or cannot be opened', [ZipPath]));

  TargetFolder := Shell.NameSpace(TargetPath);
  if VarIsClear(TargetFolder) then
    RaiseException(Format('Target path "%s" does not exist', [TargetPath]));

  TargetFolder.CopyHere(
    ZipFile.Items, SHCONTCH_NOPROGRESSBOX or SHCONTCH_RESPONDYESTOALL);
end;

var ROMFilePage: TInputFileWizardPage;
var R : longint;
var rom: string;
var MinecraftDownloadPage: TDownloadWizardPage;

procedure AddRomPage();
begin
  rom := FileSearch('Zelda no Densetsu - Kamigami no Triforce (Japan).sfc', WizardDirValue());
  if Length(rom) > 0 then
    begin
      log('existing ROM found');
      log(IntToStr(CompareStr(GetMD5OfFile(rom), '03a63945398191337e896e5771f77173')));
      if CompareStr(GetMD5OfFile(rom), '03a63945398191337e896e5771f77173') = 0 then
        begin
        log('existing ROM verified');
        exit;
        end;
      log('existing ROM failed verification');
    end;
  rom := ''
  ROMFilePage :=
    CreateInputFilePage(
      wpSelectComponents,
      'Select ROM File',
      'Where is your Zelda no Densetsu - Kamigami no Triforce (Japan).sfc located?',
      'Select the file, then click Next.');

  ROMFilePage.Add(
    'Location of ROM file:',
    'SNES ROM files|*.sfc|All files|*.*',
    '.sfc');
end;

procedure AddMinecraftDownloads();
begin
  MinecraftDownloadPage := CreateDownloadPage(SetupMessage(msgWizardPreparing), SetupMessage(msgPreparingDesc), @OnDownloadMinecraftProgress);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if (CurPageID = wpReady) and (WizardIsComponentSelected('client/minecraft')) then begin
    MinecraftDownloadPage.Clear;
    if(IsForgeNeeded()) then
      MinecraftDownloadPage.Add('https://maven.minecraftforge.net/net/minecraftforge/forge/'+FORGE_VERSION+'/forge-'+FORGE_VERSION+'-installer.jar','forge-installer.jar','');
    if(IsJavaNeedeD()) then
      MinecraftDownloadPage.Add('https://corretto.aws/downloads/latest/amazon-corretto-8-x64-windows-jre.zip','java.zip','');
    MinecraftDownloadPage.Show;
    try
      try
        MinecraftDownloadPage.Download;
        Result := True;
      except
        if MinecraftDownloadPage.AbortedByUser then
          Log('Aborted by user.')
        else
          SuppressibleMsgBox(AddPeriod(GetExceptionMessage), mbCriticalError, MB_OK, IDOK);
        Result := False;
      end;
    finally
      if( isJavaNeeded() ) then
        UnZip(ExpandConstant('{tmp}')+'\java.zip',ExpandConstant('{app}'));
      MinecraftDownloadPage.Hide;
    end;
    Result := True;
  end else
    Result := True;
end;

procedure InitializeWizard();
begin
  AddRomPage();
  AddMinecraftDownloads();
end;


function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  if (assigned(ROMFilePage)) and (PageID = ROMFilePage.ID) then
    Result := not (WizardIsComponentSelected('client/lttp') or WizardIsComponentSelected('generator'));
end;

function GetROMPath(Param: string): string;
begin
  if Length(rom) > 0 then
    Result := rom
  else if Assigned(RomFilePage) then
    begin
      R := CompareStr(GetMD5OfFile(ROMFilePage.Values[0]), '03a63945398191337e896e5771f77173')
      if R <> 0 then
        MsgBox('ROM validation failed. Very likely wrong file.', mbInformation, MB_OK);
  
      Result := ROMFilePage.Values[0]
    end
  else
    Result := '';
 end;
