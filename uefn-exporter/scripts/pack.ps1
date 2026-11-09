param([Parameter(Mandatory = $true)][string]$Step, [string]$Name = '', [string]$Text = '', [int]$X = 0, [int]$Y = 0,
      [string]$Root = 'H:\UnrealToUEFN\UnrealProjects')	# the folder the UE projects are made in
# Steps of the Fab pack -> UEFN pipeline (8.10.2026), so each pack is a few calls. Process: memory file ucitavanjeSaFaba.md
$ErrorActionPreference = 'Stop'
$scratch = $PSScriptRoot
$screen = Join-Path $scratch 'screen.ps1'
$ue = 'J:\EpicGamesDownloadFiles\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe'
$uefn = 'C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe'
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class PackMouse {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
}
"@
[PackMouse]::SetProcessDPIAware() | Out-Null

function Front($proc) { $p = Get-Process $proc -ErrorAction SilentlyContinue | Select-Object -First 1; if ($p) { $w = New-Object -ComObject WScript.Shell; $null = $w.AppActivate($p.Id); Start-Sleep -Milliseconds 700 } }
function Click($x, $y) { & $screen -ClickX $x -ClickY $y | Out-Null }
function SendText($t) { [System.Windows.Forms.SendKeys]::SendWait($t) }

switch ($Step) {
  'closeall' {
    Get-Process | Where-Object { $_.ProcessName -like 'FortniteClient*' -or $_.ProcessName -like 'UnrealEditorFortnite*' -or $_.ProcessName -eq 'FortniteLauncher' -or $_.ProcessName -eq 'CrashReportClientEditor' } | Stop-Process -Force
    Start-Sleep 4; 'closed'
  }
  'newue' {   # create the source UE project from the saved template (Lumen + distance fields) and open it
    $root = "$Root\$Name"
    if (-not (Test-Path $root)) {
      New-Item -ItemType Directory -Force "$root\Config", "$root\Content", "$root\Plugins" | Out-Null
      Copy-Item "$PSScriptRoot\ProjectTemplate\Config\*.ini" "$root\Config\"
      Copy-Item "$PSScriptRoot\ProjectTemplate\Template.uproject" "$root\$Name.uproject"
      $g = "$root\Config\DefaultGame.ini"; $t = Get-Content $g -Raw
      $t = $t -replace 'ProjectID=[0-9A-F]+', ('ProjectID=' + ([guid]::NewGuid().ToString('N').ToUpper())) -replace 'ProjectName=\w+', "ProjectName=$Name"
      Set-Content -Path $g -Value $t -NoNewline -Encoding ascii
      cmd /c mklink /J "$root\Plugins\UE_MCP_Bridge" 'H:\UnrealToUEFN\Plugin\UE_MCP_Bridge' | Out-Null
    }
    $p = Start-Process -FilePath $ue -ArgumentList "`"$root\$Name.uproject`"" -PassThru; "UE pid $($p.Id)"
  }
  'openue' { $p = Start-Process -FilePath $ue -ArgumentList "`"$Root\$Name\$Name.uproject`"" -PassThru; "UE pid $($p.Id)" }
  'fabsearch' {   # Fab window (floating Content Browser remembers it) -> My Library -> search text
    Front 'UnrealEditor'; Click 300 74; Click 346 196; Start-Sleep 5
    & $screen | Out-Null; 'fab opened'
  }
  'mylib' { Click 1658 272; Start-Sleep 3; Click 1200 272; SendText $Text; Start-Sleep 2; Click 956 317; Start-Sleep 4; & $screen | Out-Null; 'searched' }
  'click' { Click $X $Y; Start-Sleep 2; & $screen | Out-Null; 'clicked' }
  'dblclick' { & $screen -ClickX $X -ClickY $Y -Double | Out-Null; 'dbl' }
  'shot' { & $screen | Out-Null; 'shot' }
  'uefnstart' { $a = if ($Name) { "`"H:/UnrealToUEFN/UEFN/$Name/$Name.uefnproject`"" } else { '' }
    $p = if ($a) { Start-Process -FilePath $uefn -ArgumentList $a -PassThru } else { Start-Process -FilePath $uefn -PassThru }; "UEFN pid $($p.Id)" }
  'uefntile' {   # picker maximized, then the first Recent Projects tile (the project just opened)
    # Windows keeps another app (Discord) in front of a window a script activates: everything is minimized and UEFN maximized again
    (New-Object -ComObject Shell.Application).MinimizeAll(); Start-Sleep 2
    $p = Get-Process UnrealEditorFortnite-Win64-Shipping | Select-Object -First 1; [PackMouse]::ShowWindow($p.MainWindowHandle, 3) | Out-Null; Start-Sleep 2
    Front 'UnrealEditorFortnite-Win64-Shipping'; Click 654 280; Start-Sleep 1; & $screen -ClickX 654 -ClickY 280 -Double | Out-Null; 'tile'  # the first click of a window not in front only focuses it (Garage, 8.10)
  }
  'uefnnew' {   # picker maximized -> New Project -> Blank -> name -> Create
    $p = Get-Process UnrealEditorFortnite-Win64-Shipping | Select-Object -First 1; [PackMouse]::ShowWindow($p.MainWindowHandle, 3) | Out-Null; Start-Sleep 2
    Front 'UnrealEditorFortnite-Win64-Shipping'; Click 144 236; Start-Sleep 3; Click 1146 270; Start-Sleep 1
    Click 1680 904; SendText '^a'; Start-Sleep -Milliseconds 300; SendText $Name; Start-Sleep 1
    & $screen -Out (Join-Path $scratch 'new_named.png') | Out-Null; Click 1786 975; 'create clicked'
  }
  'uefnmaps' {   # popups closed, Content Browser, Add > New Folder Maps, map tile (-X) dragged onto it, Move Here, OK
    Front 'UnrealEditorFortnite-Win64-Shipping'; Start-Sleep 1
    Click 1440 222; Start-Sleep -Milliseconds 500; Click 2092 392; Start-Sleep -Milliseconds 500; Click 78 574; Start-Sleep 1
    Click 282 607; Start-Sleep 1; Click 392 388; Start-Sleep 1; SendText 'Maps'; SendText '{ENTER}'; Start-Sleep 2
    & $screen -Out (Join-Path $scratch 'maps_folder.png') | Out-Null
    [PackMouse]::SetCursorPos($X, 735) | Out-Null; Start-Sleep -Milliseconds 200
    [PackMouse]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 200
    $steps = 20; foreach ($i in 1..$steps) { [PackMouse]::SetCursorPos([int]($X - ($X - 296) * $i / $steps), 735) | Out-Null; Start-Sleep -Milliseconds 30 }
    Start-Sleep -Milliseconds 300; [PackMouse]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep 1
    & $screen -Out (Join-Path $scratch 'maps_drop.png') | Out-Null
    Click 358 777; Start-Sleep 2; Click 1402 592
    for ($i = 0; $i -lt 60; $i++) { if (Test-Path "H:\UnrealToUEFN\UEFN\$Name\Content\Maps\$Name.umap") { break }; Start-Sleep 1 }
    if (-not (Test-Path "H:\UnrealToUEFN\UEFN\$Name\Content\Maps\$Name.umap")) { 'MAP NOT MOVED'; return }
    Start-Sleep 5
    [PackMouse]::SetCursorPos(96, 703) | Out-Null; Start-Sleep -Milliseconds 200
    [PackMouse]::mouse_event(8, 0, 0, 0, [UIntPtr]::Zero); [PackMouse]::mouse_event(16, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep 1
    Click 232 552; Start-Sleep 3; & $screen -Out (Join-Path $scratch 'redirectors.png') | Out-Null
    Click 1036 904; Start-Sleep 3; & $screen -Out (Join-Path $scratch 'maps_done.png') | Out-Null; 'map moved'
  }
  'uefnfront' { Front 'UnrealEditorFortnite-Win64-Shipping'; & $screen | Out-Null; 'front' }
  'newproject' {   # picker -> New Project -> Blank -> name -> Create
    Front 'UnrealEditorFortnite-Win64-Shipping'; Click 782 375; Start-Sleep 3; Click 1146 264; Start-Sleep 1
    Click 1680 904; SendText '^a'; Start-Sleep -Milliseconds 300; SendText $Name; Start-Sleep 1
    & $screen | Out-Null; 'named'
  }
  'create' { Click 1786 975; 'create clicked' }
  'mapsfolder' {   # close the popups, Content Browser, Add > New Folder "Maps", drag the map into it, Move Here, OK
    Front 'UnrealEditorFortnite-Win64-Shipping'; Start-Sleep 2
    Click 1440 218; Start-Sleep -Milliseconds 400; Click 2093 393; Start-Sleep -Milliseconds 400; Click 78 574; Start-Sleep 1
    Click 282 607; Start-Sleep -Milliseconds 700; Click 392 388; Start-Sleep -Milliseconds 700; SendText 'Maps'; SendText '{ENTER}'; Start-Sleep 2
    [PackMouse]::SetCursorPos(500, 735) | Out-Null; Start-Sleep -Milliseconds 200
    [PackMouse]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 200
    foreach ($i in 1..20) { [PackMouse]::SetCursorPos(500 - $i * 10, 735) | Out-Null; Start-Sleep -Milliseconds 30 }
    Start-Sleep -Milliseconds 300; [PackMouse]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep 1
    & $screen | Out-Null; 'dragged'
  }
  'movehere' {
    Click 358 777; Start-Sleep 2; Click 1402 593
    for ($i = 0; $i -lt 60; $i++) { if (Test-Path "H:\UnrealToUEFN\UEFN\$Name\Content\Maps\$Name.umap") { break }; Start-Sleep 1 }
    Start-Sleep 5
    [PackMouse]::SetCursorPos(100, 703) | Out-Null; Start-Sleep -Milliseconds 200
    [PackMouse]::mouse_event(8, 0, 0, 0, [UIntPtr]::Zero); [PackMouse]::mouse_event(16, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep 1
    Click 236 553; Start-Sleep 3; & $screen | Out-Null; 'redirector report'
  }
  'delredir' { Click 1036 905; Start-Sleep 3; & $screen | Out-Null; 'deleted' }
  'exituefn' {
    Front 'UnrealEditorFortnite-Win64-Shipping'; Click 76 10; Start-Sleep -Milliseconds 800; Click 116 368
    for ($i = 0; $i -lt 60; $i++) { if (-not (Get-Process UnrealEditorFortnite-Win64-Shipping -ErrorAction SilentlyContinue)) { break }; Start-Sleep 1 }
    if (Get-Process UnrealEditorFortnite-Win64-Shipping -ErrorAction SilentlyContinue) { 'UEFN still running' } else { 'UEFN closed' }
  }
  'launch' { Front 'UnrealEditorFortnite-Win64-Shipping'; Click 2093 393; Start-Sleep -Milliseconds 500; Click 732 77; 'launch clicked' }
  'gameshot' { Front 'FortniteClient-Win64-Shipping'; & $screen -Out (Join-Path $scratch "$Name`_session.png") | Out-Null; 'game shot' }
  default { "unknown step $Step" }
}
