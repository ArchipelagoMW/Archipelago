#define source_path ReadIni(SourcePath + "\setup.ini", "Data", "source_path")
#define min_windows ReadIni(SourcePath + "\setup.ini", "Data", "min_windows")

#define MyAppName "Archipelago"
#define MyAppExeName "ArchipelagoServer.exe"
#define MyAppIcon "data/icon.ico"
#dim VersionTuple[4]
#define MyAppVersion ParseVersion(source_path + '\ArchipelagoServer.exe', VersionTuple[0], VersionTuple[1], VersionTuple[2], VersionTuple[3])
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
; you will likely have to remove the following signtool line when testing/debugging locally. Don't include that change in PRs.
SignTool= signtool
LicenseFile= LICENSE
WizardStyle= modern
SetupLogging=yes
MinVersion={#min_windows}

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
Name: "core";             Description: "Core Files"; Types: full hosting playing custom; Flags: fixed
Name: "generator";        Description: "Generator"; Types: full hosting
Name: "generator/sm";     Description: "Super Metroid ROM Setup"; Types: full hosting; ExtraDiskSpaceRequired: 3145728; Flags: disablenouninstallwarning
Name: "generator/soe";    Description: "Secret of Evermore ROM Setup"; Types: full hosting; ExtraDiskSpaceRequired: 3145728; Flags: disablenouninstallwarning
Name: "generator/lttp";   Description: "A Link to the Past ROM Setup and Enemizer"; Types: full hosting; ExtraDiskSpaceRequired: 5191680
Name: "generator/oot";    Description: "Ocarina of Time ROM Setup"; Types: full hosting; ExtraDiskSpaceRequired: 100663296; Flags: disablenouninstallwarning
Name: "server";           Description: "Server"; Types: full hosting
Name: "client";           Description: "Clients"; Types: full playing
Name: "client/sni";       Description: "SNI Client"; Types: full playing
Name: "client/sni/lttp";  Description: "SNI Client - A Link to the Past Patch Setup"; Types: full playing; Flags: disablenouninstallwarning
Name: "client/sni/sm";    Description: "SNI Client - Super Metroid Patch Setup"; Types: full playing; Flags: disablenouninstallwarning
Name: "client/factorio";  Description: "Factorio"; Types: full playing
Name: "client/minecraft"; Description: "Minecraft"; Types: full playing; ExtraDiskSpaceRequired: 226894278
Name: "client/oot";       Description: "Ocarina of Time Adjuster"; Types: full playing
Name: "client/ff1";       Description: "Final Fantasy 1"; Types: full playing
Name: "client/text";      Description: "Text, to !command and chat"; Types: full playing

[Dirs]
NAME: "{app}"; Flags: setntfscompression; Permissions: everyone-modify users-modify authusers-modify;

[Files]
Source: "{code:GetROMPath}"; DestDir: "{app}"; DestName: "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"; Flags: external; Components: client/sni/lttp or generator/lttp
Source: "{code:GetSMROMPath}"; DestDir: "{app}"; DestName: "Super Metroid (JU).sfc"; Flags: external; Components: client/sni/sm or generator/sm
Source: "{code:GetSoEROMPath}"; DestDir: "{app}"; DestName: "Secret of Evermore (USA).sfc"; Flags: external; Components: generator/soe
Source: "{code:GetOoTROMPath}"; DestDir: "{app}"; DestName: "The Legend of Zelda - Ocarina of Time.z64"; Flags: external; Components: generator/oot
Source: "{#source_path}\*"; Excludes: "*.sfc, *.log, data\sprites\alttpr, SNI, EnemizerCLI, Archipelago*.exe"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#source_path}\SNI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\SNI"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: client/sni
Source: "{#source_path}\EnemizerCLI\*"; Excludes: "*.sfc, *.log"; DestDir: "{app}\EnemizerCLI"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: generator/lttp

Source: "{#source_path}\ArchipelagoGenerate.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: generator
Source: "{#source_path}\ArchipelagoServer.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: server
Source: "{#source_path}\ArchipelagoFactorioClient.exe";  DestDir: "{app}"; Flags: ignoreversion; Components: client/factorio
Source: "{#source_path}\ArchipelagoTextClient.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/text
Source: "{#source_path}\ArchipelagoSNIClient.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/sni
Source: "{#source_path}\ArchipelagoLttPAdjuster.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/sni/lttp or generator/lttp
Source: "{#source_path}\ArchipelagoMinecraftClient.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/minecraft
Source: "{#source_path}\ArchipelagoOoTAdjuster.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/oot
Source: "{#source_path}\ArchipelagoFF1Client.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: client/ff1
Source: "vc_redist.x64.exe"; DestDir: {tmp}; Flags: deleteafterinstall

[Icons]
Name: "{group}\{#MyAppName} Folder"; Filename: "{app}";
Name: "{group}\{#MyAppName} Server"; Filename: "{app}\{#MyAppExeName}"; Components: server
Name: "{group}\{#MyAppName} Text Client"; Filename: "{app}\ArchipelagoTextClient.exe"; Components: client/text
Name: "{group}\{#MyAppName} SNI Client"; Filename: "{app}\ArchipelagoSNIClient.exe"; Components: client/sni
Name: "{group}\{#MyAppName} Factorio Client"; Filename: "{app}\ArchipelagoFactorioClient.exe"; Components: client/factorio
Name: "{group}\{#MyAppName} Minecraft Client"; Filename: "{app}\ArchipelagoMinecraftClient.exe"; Components: client/minecraft
Name: "{group}\{#MyAppName} Final Fantasy 1 Client"; Filename: "{app}\ArchipelagoFF1Client.exe"; Components: client/ff1

Name: "{commondesktop}\{#MyAppName} Folder"; Filename: "{app}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName} Server"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Components: server
Name: "{commondesktop}\{#MyAppName} SNI Client"; Filename: "{app}\ArchipelagoSNIClient.exe"; Tasks: desktopicon; Components: client/sni
Name: "{commondesktop}\{#MyAppName} Factorio Client"; Filename: "{app}\ArchipelagoFactorioClient.exe"; Tasks: desktopicon; Components: client/factorio
Name: "{commondesktop}\{#MyAppName} Final Fantasy 1 Client"; Filename: "{app}\ArchipelagoFF1Client.exe"; Tasks: desktopicon; Components: client/factorio

[Run]

Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/passive /norestart"; Check: IsVCRedist64BitNeeded; StatusMsg: "Installing VC++ redistributable..."
Filename: "{app}\ArchipelagoLttPAdjuster"; Parameters: "--update_sprites"; StatusMsg: "Updating Sprite Library..."; Components: client/sni/lttp or generator/lttp
Filename: "{app}\ArchipelagoMinecraftClient.exe"; Parameters: "--install"; StatusMsg: "Installing Forge Server..."; Components: client/minecraft

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[InstallDelete]
Type: files; Name: "{app}\ArchipelagoLttPClient.exe"

[Registry]

Root: HKCR; Subkey: ".apbp";                                 ValueData: "{#MyAppName}patch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}patch";                     ValueData: "Archipelago Binary Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}patch\DefaultIcon";         ValueData: "{app}\ArchipelagoSNIClient.exe,0";                           ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}patch\shell\open\command";  ValueData: """{app}\ArchipelagoSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: ""; Components: client/sni

Root: HKCR; Subkey: ".apm3";                                 ValueData: "{#MyAppName}smpatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}smpatch";                     ValueData: "Archipelago Super Metroid Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}smpatch\DefaultIcon";         ValueData: "{app}\ArchipelagoSNIClient.exe,0";                           ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}smpatch\shell\open\command";  ValueData: """{app}\ArchipelagoSNIClient.exe"" ""%1""";                  ValueType: string;  ValueName: ""; Components: client/sni

Root: HKCR; Subkey: ".apsoe";                                 ValueData: "{#MyAppName}soepatch";        Flags: uninsdeletevalue; ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}soepatch";                     ValueData: "Archipelago Secret of Evermore Patch"; Flags: uninsdeletekey;   ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}soepatch\DefaultIcon";         ValueData: "{app}\ArchipelagoSNIClient.exe,0";                           ValueType: string;  ValueName: ""; Components: client/sni
Root: HKCR; Subkey: "{#MyAppName}soepatch\shell\open\command";  ValueData: """{app}\ArchipelagoSNIClient.exe"" ""%1""";

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

var R : longint;

var lttprom: string;
var LttPROMFilePage: TInputFileWizardPage;

var smrom: string;
var SMRomFilePage: TInputFileWizardPage;

var soerom: string;
var SoERomFilePage: TInputFileWizardPage;

var ootrom: string;
var OoTROMFilePage: TInputFileWizardPage;

function GetSNESMD5OfFile(const rom: string): string;
var data: AnsiString;
begin
  if LoadStringFromFile(rom, data) then
  begin
      if Length(data) mod 1024 = 512 then
      begin
        data := copy(data, 513, Length(data)-512);
      end;
      Result := GetMD5OfString(data);
  end;
end;

function CheckRom(name: string; hash: string): string;
var rom: string;
begin
  log('Handling ' + name)
  rom := FileSearch(name, WizardDirValue());
  if Length(rom) > 0 then
    begin
      log('existing ROM found');
      log(IntToStr(CompareStr(GetSNESMD5OfFile(rom), hash)));
      if CompareStr(GetSNESMD5OfFile(rom), hash) = 0 then
        begin
        log('existing ROM verified');
        Result := rom;
        exit;
        end;
      log('existing ROM failed verification');
    end;
end;

function AddRomPage(name: string): TInputFileWizardPage;
begin
  Result :=
    CreateInputFilePage(
      wpSelectComponents,
      'Select ROM File',
      'Where is your ' + name + ' located?',
      'Select the file, then click Next.');

  Result.Add(
    'Location of ROM file:',
    'SNES ROM files|*.sfc;*.smc|All files|*.*',
    '.sfc');
end;

procedure AddOoTRomPage();
begin
  ootrom := FileSearch('The Legend of Zelda - Ocarina of Time.z64', WizardDirValue());
  if Length(ootrom) > 0 then
    begin
      log('existing ROM found');
      log(IntToStr(CompareStr(GetMD5OfFile(ootrom), '5bd1fe107bf8106b2ab6650abecd54d6'))); // normal
      log(IntToStr(CompareStr(GetMD5OfFile(ootrom), '6697768a7a7df2dd27a692a2638ea90b'))); // byteswapped
      log(IntToStr(CompareStr(GetMD5OfFile(ootrom), '05f0f3ebacbc8df9243b6148ffe4792f'))); // decompressed
      if (CompareStr(GetMD5OfFile(ootrom), '5bd1fe107bf8106b2ab6650abecd54d6') = 0) or (CompareStr(GetMD5OfFile(ootrom), '6697768a7a7df2dd27a692a2638ea90b') = 0) or (CompareStr(GetMD5OfFile(ootrom), '05f0f3ebacbc8df9243b6148ffe4792f') = 0) then
        begin
        log('existing ROM verified');
        exit;
        end;
      log('existing ROM failed verification');
    end;
  ootrom := ''
  OoTROMFilePage :=
    CreateInputFilePage(
      wpSelectComponents,
      'Select ROM File',
      'Where is your OoT 1.0 ROM located?',
      'Select the file, then click Next.');

  OoTROMFilePage.Add(
    'Location of ROM file:',
    'N64 ROM files (*.z64, *.n64)|*.z64;*.n64|All files|*.*',
    '.z64');
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  if (assigned(LttPROMFilePage)) and (CurPageID = LttPROMFilePage.ID) then
    Result := not (LttPROMFilePage.Values[0] = '')
  else if (assigned(SMROMFilePage)) and (CurPageID = SMROMFilePage.ID) then
    Result := not (SMROMFilePage.Values[0] = '')
  else if (assigned(SoEROMFilePage)) and (CurPageID = SoEROMFilePage.ID) then
    Result := not (SoEROMFilePage.Values[0] = '')
  else if (assigned(OoTROMFilePage)) and (CurPageID = OoTROMFilePage.ID) then
    Result := not (OoTROMFilePage.Values[0] = '')
  else
    Result := True;
end;

function GetROMPath(Param: string): string;
begin
  if Length(lttprom) > 0 then
    Result := lttprom
  else if Assigned(LttPRomFilePage) then
    begin
      R := CompareStr(GetSNESMD5OfFile(LttPROMFilePage.Values[0]), '03a63945398191337e896e5771f77173')
      if R <> 0 then
        MsgBox('ALttP ROM validation failed. Very likely wrong file.', mbInformation, MB_OK);

      Result := LttPROMFilePage.Values[0]
    end
  else
    Result := '';
 end;

function GetSMROMPath(Param: string): string;
begin
  if Length(smrom) > 0 then
    Result := smrom
  else if Assigned(SMRomFilePage) then
    begin
      R := CompareStr(GetSNESMD5OfFile(SMROMFilePage.Values[0]), '21f3e98df4780ee1c667b84e57d88675')
      if R <> 0 then
        MsgBox('Super Metroid ROM validation failed. Very likely wrong file.', mbInformation, MB_OK);

      Result := SMROMFilePage.Values[0]
    end
  else
    Result := '';
 end;

function GetSoEROMPath(Param: string): string;
begin
  if Length(soerom) > 0 then
    Result := soerom
  else if Assigned(SoERomFilePage) then
    begin
      R := CompareStr(GetSNESMD5OfFile(SoEROMFilePage.Values[0]), '6e9c94511d04fac6e0a1e582c170be3a')
      if R <> 0 then
        MsgBox('Secret of Evermore ROM validation failed. Very likely wrong file.', mbInformation, MB_OK);

      Result := SoEROMFilePage.Values[0]
    end
  else
    Result := '';
 end;

function GetOoTROMPath(Param: string): string;
begin
  if Length(ootrom) > 0 then
    Result := ootrom
  else if Assigned(OoTROMFilePage) then
    begin
      R := CompareStr(GetMD5OfFile(OoTROMFilePage.Values[0]), '5bd1fe107bf8106b2ab6650abecd54d6') * CompareStr(GetMD5OfFile(OoTROMFilePage.Values[0]), '6697768a7a7df2dd27a692a2638ea90b') * CompareStr(GetMD5OfFile(OoTROMFilePage.Values[0]), '05f0f3ebacbc8df9243b6148ffe4792f');
      if R <> 0 then
        MsgBox('OoT ROM validation failed. Very likely wrong file.', mbInformation, MB_OK);

      Result := OoTROMFilePage.Values[0]
    end
  else
    Result := '';
end;

procedure InitializeWizard();
begin
  AddOoTRomPage();

  lttprom := CheckRom('Zelda no Densetsu - Kamigami no Triforce (Japan).sfc', '03a63945398191337e896e5771f77173');
  if Length(lttprom) = 0 then
    LttPROMFilePage:= AddRomPage('Zelda no Densetsu - Kamigami no Triforce (Japan).sfc');

  smrom := CheckRom('Super Metroid (JU).sfc', '21f3e98df4780ee1c667b84e57d88675');
  if Length(smrom) = 0 then
    SMRomFilePage:= AddRomPage('Super Metroid (JU).sfc');

  soerom := CheckRom('Secret of Evermore (USA).sfc', '6e9c94511d04fac6e0a1e582c170be3a');
  if Length(soerom) = 0 then
    SoEROMFilePage:= AddRomPage('Secret of Evermore (USA).sfc');
end;


function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  if (assigned(LttPROMFilePage)) and (PageID = LttPROMFilePage.ID) then
    Result := not (WizardIsComponentSelected('client/sni/lttp') or WizardIsComponentSelected('generator/lttp'));
  if (assigned(SMROMFilePage)) and (PageID = SMROMFilePage.ID) then
    Result := not (WizardIsComponentSelected('client/sni/sm') or WizardIsComponentSelected('generator/sm'));
  if (assigned(SoEROMFilePage)) and (PageID = SoEROMFilePage.ID) then
    Result := not (WizardIsComponentSelected('generator/soe'));
  if (assigned(OoTROMFilePage)) and (PageID = OoTROMFilePage.ID) then
    Result := not (WizardIsComponentSelected('generator/oot'));
end;