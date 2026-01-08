Invoke-WebRequest -Uri https://github.com/Ijwu/Enemizer/releases/download/7.1/win-x64.zip -OutFile enemizer.zip
Expand-Archive -Path enemizer.zip -DestinationPath EnemizerCLI -Force
choco install innosetup --version=6.2.2 --allow-downgrade
py -m pip install --upgrade pip
py setup.py build_exe --yes
if ( $? -eq $false ) {
  Write-Error "setup.py failed!"
  exit 1
}
$NAME="$(ls build | Select-String -Pattern 'exe')".Split('.',2)[1]
$ZIP_NAME="Archipelago_$NAME.7z"
echo "$NAME -> $ZIP_NAME"
echo "ZIP_NAME=$ZIP_NAME" >> $Env:GITHUB_ENV
New-Item -Path dist -ItemType Directory -Force
cd build
Rename-Item "exe.$NAME" Archipelago
$7zipPath = "$env:ProgramFiles\7-Zip\7z.exe"
Set-Alias Start-SevenZip $7zipPath
Start-SevenZip a -mx=9 -mhe=on -ms "../dist/$ZIP_NAME" Archipelago
Rename-Item Archipelago "exe.$NAME"  # inno_setup.iss expects the original name

& "${env:ProgramFiles(x86)}\Inno Setup 6\iscc.exe" ../inno_setup.iss /DNO_SIGNTOOL
if ( $? -eq $false ) {
  Write-Error "Building setup failed!"
  exit 1
}