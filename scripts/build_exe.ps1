$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

pyinstaller `
  --noconfirm `
  --clean `
  --onefile `
  --name horloge `
  main.py

Write-Host "Binary generated in dist/horloge.exe"
