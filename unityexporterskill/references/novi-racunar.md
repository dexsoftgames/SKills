# Na drugom računaru

## Šta treba
- Unreal Engine 5.8 (na glavnom: `J:\EpicGamesDownloadFiles\UE_5.8`). Exporter ide u `<UE>\Engine\Plugins\Marketplace\UnrealToUnityExporterWithLandscape` (EnabledByDefault). Na drugom računaru putanja engine-a može biti drugačija — proveri `RunUAT`/`Engine` pre skripti (`install_exporter_to_engine.ps1` ima tvrdo upisan J: put).
- Unity 6 + URP 17, Color Space Linear, Input System (activeInputHandler 1).
- MCP: ue-mcp (Unreal most, plugin UE_MCP_Bridge), MCP for Unity (port 8080), unreal-epic (port 8000). Ako unity MCP ne može: HTTP JSON-RPC na 127.0.0.1:8080/mcp; ako ue-mcp ne može: Python remote execution (bRemoteExecution=True).
- Python 3 (skripte), PowerShell.

## Instalacija svega
- `L:\8TB\DEXSOFT Plugins\INSTALIRAJ_SVE.bat` → `SVIMCPSERVERI\Setup.ps1` (offline): programi, MCP serveri, Unreal pluginovi iz `DexsoftPlugins\Unreal\*.zip` (uključujući UnrealToUnityExporterWithLandscape_1.0.zip) u Marketplace, Unity paketi, i **Claude Code settings/hooks/skills/memorija iz `SVIMCPSERVERI\Claude\`**.
- Dokaz rada: `Setup_<RACUNAR>_full.log` i `Setup_<RACUNAR>.log`. Admin proces ne vidi mapiran mrežni disk → Elevate.ps1; .msi preko mreže se prvo kopira u TEMP.
- Exporter u postojećem Unrealu: dugme „Check latest UnityExporter" instalira najnoviji zip sa 8TB.
- Importer u Unity projektu: `Packages/manifest.json` → `"com.dexsoft.import-unreal-scene": "file:<putanja do tgz>"` (na glavnom: L:/8TB/.../UnityPackage/com.dexsoft.import-unreal-scene-1.0.0.tgz).

## Putanje koje su vezane za glavni računar
- `H:\UnrealToUnityExporter\` (izvor, projekti, UnityProject, UnityExports, skripte), `H:\UTUB\` (build), `L:\8TB\DEXSOFT Plugins\` (release, mrežno `\\Dexveliki\8TB\...`). Na drugom računaru pitaj gde su, ne pretpostavljaj.
- Izvor koda postoji SAMO na glavnom računaru (H:). Na drugom se radi sa gotovim zipom/tgz-om; izmene koda idu na glavnom.

## Ovaj skill
- Leži u `%USERPROFILE%\.claude\skills\unityexporterskill\` i u `L:\8TB\DEXSOFT Plugins\SVIMCPSERVERI\Claude\skills\unityexporterskill\` (Setup.ps1 ga kopira na svaki računar). Kad se znanje promeni, osveži OBE kopije.
