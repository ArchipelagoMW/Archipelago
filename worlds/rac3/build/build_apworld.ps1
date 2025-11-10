$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$parentDir = Split-Path -Parent $scriptDir
$grandParentDir = Split-Path -Parent $parentDir
Set-Location $grandParentDir

$zipPath = Join-Path $PWD "rac3.zip"
$apworldPath = Join-Path $PWD "rac3.apworld"
$sourceFolder = Join-Path $PWD "rac3"
$outputPath = Join-Path $scriptDir "rac3.apworld"

Write-Host "Preparing to zip rac3 folder..."
if (Test-Path $zipPath) {
    Write-Host "Removing existing rac3.zip..."
    Remove-Item $zipPath
}
if (Test-Path $apworldPath) {
    Write-Host "Removing existing rac3.apworld..."
    Remove-Item $apworldPath
}

Compress-Archive -Path $sourceFolder -DestinationPath $zipPath -Force
Write-Host "Renaming rac3.zip to rac3.apworld..."
Rename-Item -Path $zipPath -NewName "rac3.apworld"
Write-Host "Moving rac3.apworld to script directory..."
Move-Item -Path $apworldPath -Destination $outputPath -Force
Write-Host "Done! Output: $outputPath"