param([int]$TimeoutSec = 1500)
# Watches a UEFN Launch Session: clicks "Make Private" as soon as that dialog shows, stops on validation failure,
# ends when the Fortnite client reports the match in progress. Prints one line per event.
Add-Type @"
using System; using System.Text; using System.Collections.Generic; using System.Runtime.InteropServices;
public static class UW {
    public delegate bool EnumProc(IntPtr h, IntPtr l);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc p, IntPtr l);
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    public static List<string> Titles(uint pid) {
        var list = new List<string>();
        EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p);
            if (p == pid && IsWindowVisible(h)) { var sb = new StringBuilder(256); GetWindowText(h, sb, 256); if (sb.Length > 0) list.Add(sb.ToString()); }
            return true; }, IntPtr.Zero);
        return list;
    }
    // The first click only focuses a window that is not in front; the second presses the button
    public static void Click(int x, int y) { SetCursorPos(x, y); System.Threading.Thread.Sleep(150); mouse_event(2,0,0,0,UIntPtr.Zero); mouse_event(4,0,0,0,UIntPtr.Zero);
        System.Threading.Thread.Sleep(400); mouse_event(2,0,0,0,UIntPtr.Zero); mouse_event(4,0,0,0,UIntPtr.Zero); }
}
"@
[UW]::SetProcessDPIAware() | Out-Null
$editorLog = "$env:LOCALAPPDATA\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log"
$clientLog = "$env:LOCALAPPDATA\FortniteGame\Saved\Logs\FortniteGame.log"
$start = Get-Date
$clicked = 0
while (((Get-Date) - $start).TotalSeconds -lt $TimeoutSec) {
    $uefn = Get-Process | Where-Object { $_.ProcessName -like "UnrealEditorFortnite*" } | Select-Object -First 1
    if (-not $uefn) { "UEFN_GONE"; exit 1 }
    $titles = [UW]::Titles([uint32]$uefn.Id)
    # A large pack lists thousands of assets and the dialog takes a while to answer clicks (BasketballArena,
    # 8.10.2026: six clicks in the first minute all missed), so it is tried for longer
    if ($titles -contains "Make Assets Private" -and $clicked -lt 30) {
        Start-Sleep 5
        [UW]::Click(1134, 856); $clicked++; "CLICKED Make Private"
    }
    if ($titles -contains "Unable to Play") { "UNABLE_TO_PLAY"; exit 2 }
    $tail = Get-Content $editorLog -Tail 400 -ErrorAction SilentlyContinue
    if ($tail -match "Validation failed|FlowStep_RunLocalValidation\(\): Fail") { "VALIDATION_FAILED"; exit 2 }
    if (Test-Path $clientLog) {
        $item = Get-Item $clientLog
        if ($item.LastWriteTime -gt $start -and (Select-String -Path $clientLog -Pattern "Match State Changed from WaitingToStart to InProgress" -Quiet)) {
            if ((Get-Content $clientLog -TotalCount 5 | Out-String) -ne "" -and $item.CreationTime -gt $start.AddMinutes(-1)) { "INGAME"; exit 0 }
        }
    }
    Start-Sleep 10
}
"TIMEOUT"; exit 3
