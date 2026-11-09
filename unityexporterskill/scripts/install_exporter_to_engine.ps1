# Installs the freshly built Unity exporter (H:\UTUB package) into the UE 5.8 engine
# (Engine\Plugins\Marketplace), switched on for every project. All Unreal editors must be closed.
# Usage: powershell -ExecutionPolicy Bypass -File install_exporter_to_engine.ps1
$pkg = 'H:\UTUB\UnrealToUnityExporterWithLandscape'
$dst = 'J:\EpicGamesDownloadFiles\UE_5.8\Engine\Plugins\Marketplace\UnrealToUnityExporterWithLandscape'
$src = 'H:\UnrealToUnityExporter\Plugins\UnrealToUnityExporterWithLandscape'
if (Get-Process UnrealEditor -ErrorAction SilentlyContinue) { 'EDITOR RUNNING - close all Unreal editors first'; exit 1 }
if (-not (Test-Path "$pkg\Binaries\Win64")) { 'NO BUILD at ' + $pkg; exit 1 }
if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
New-Item -ItemType Directory $dst | Out-Null
foreach ($d in 'Binaries', 'Source', 'Resources') { if (Test-Path "$pkg\$d") { robocopy "$pkg\$d" "$dst\$d" /E /XF *.pdb /NFL /NDL /NJH /NJS /NP | Out-Null } }
robocopy "$src\Config" "$dst\Config" /E /NFL /NDL /NJH /NJS /NP | Out-Null
$u = Get-Content "$pkg\UnrealToUnityExporterWithLandscape.uplugin" -Raw | ConvertFrom-Json
$u | Add-Member -NotePropertyName EnabledByDefault -NotePropertyValue $true -Force
[System.IO.File]::WriteAllText("$dst\UnrealToUnityExporterWithLandscape.uplugin", ($u | ConvertTo-Json -Depth 10), (New-Object System.Text.UTF8Encoding($false)))
$dll = Get-Item "$dst\Binaries\Win64\UnrealEditor-UnrealToUnityExporterWithLandscape.dll"
"installed: $($dll.LastWriteTime)"
