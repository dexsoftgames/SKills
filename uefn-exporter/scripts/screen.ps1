param([string]$Out = "$PSScriptRoot\screen.png", [int]$ClickX = -1, [int]$ClickY = -1, [switch]$Double)
# Screenshot of the whole desktop, and optionally a (double) click at a screen point.
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class UEFNMouse {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    public static void Click() { mouse_event(0x02, 0, 0, 0, UIntPtr.Zero); mouse_event(0x04, 0, 0, 0, UIntPtr.Zero); }
}
"@
[UEFNMouse]::SetProcessDPIAware() | Out-Null
if ($ClickX -ge 0) {
    [UEFNMouse]::SetCursorPos($ClickX, $ClickY) | Out-Null
    Start-Sleep -Milliseconds 150
    [UEFNMouse]::Click()
    if ($Double) { Start-Sleep -Milliseconds 90; [UEFNMouse]::Click() }
    Start-Sleep -Milliseconds 800
}
$bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bmp.Size)
$small = New-Object System.Drawing.Bitmap $bmp, ([int]($bounds.Width / 2)), ([int]($bounds.Height / 2))
$small.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
"screen $($bounds.Left),$($bounds.Top) $($bounds.Width)x$($bounds.Height) saved at half size"
