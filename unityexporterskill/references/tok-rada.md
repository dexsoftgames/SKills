# Tok rada — Fab paket do gotovog Unity projekta

## 1. Novi UE projekat za Fab paket
- `H:\UnrealToUnityExporter\UnrealProjects\<Ime>` — **ime ≤ 20 znakova** (UE inače upozorava da snimanje može pući: MedievalVillageMEGApack → MedievalVillageMEGA).
- Config i .uproject po uzoru na postojeći projekat (npr. PodcastStudio); `.uproject` UTF-8 **BEZ BOM-a** (inače ue-mcp `set_project` pukne na JSON-u).
- Exporter je ENGINE plugin (Marketplace, EnabledByDefault) — NE treba junction ni upis u .uproject. `UE_MCP_Bridge` ide kao junction ka `H:\UnrealToUnityExporter\Plugins\UE_MCP_Bridge` (prazan Plugins/UE_MCP_Bridge folder = „Missing plugin" → zameni junction-om).
- Preuzimanje sa Faba: postupak u memoriji „ucitavanjeSaFaba" / `H:\UnrealToUEFN\Docs\FabUcitavanje`. Dok se skida, može se raditi Unity strana.
- Pre exporta proveri da paketu ne fale teksture (asset registry `get_dependencies` + `does_asset_exist`); Fab ume da isporuči paket bez stotina tekstura (MEGA pack: 319, šahovnica već u Unrealu).
- ue-mcp `start_editor` otvara projekat na koji je most vezan, ne projectPath → prvo `project(set_project)`.

## 2. Pre exporta
- Učitaj PRAVU mapu (ne Overview/showcase): `level(load, levelPath)`. Posle starta editor je na `/Temp/Untitled`.
- Čekaj šejdere: `editor(get_engine_state)` → `compiling.shaders == 0 && compiling.assets == 0`, i log `Saved/Logs/<P>.log` miruje (broj linija sa shader|compil isti 4×10 s). Svež Fab projekat zna da kompajlira 400+ asseta.
- MasterMaterialFixer sam ispravlja Dexsoft mastere pre exporta (roughness × multiplier, AO na off strani, idempotentno).

## 3. Export
- `editor(execute_command, "ExportSceneToUnity")` (ili `ExportSceneToUnity <folder>`; default `<Projekat>/UnityExport`). MCP vrati „modal dialog blocking" — to je progres prozor samog exporta, normalno.
- Čekaj da se `UnityExport/manifest.json` osveži (mtime). Exporter čisti svoje podfoldere pre pisanja.
- Izveštaj je u logu kao `LogExportToUnity: Warning: ...` (po materijalu, nebo, čestice...). Prozor sa izveštajem se pojavljuje u editoru — ne potiskivati ga (dialog policy).
- Cancel u progres prozoru prekida export čisto; sledeći export prepisuje.

## 4. Unity uvoz
- Pre uvoza: Unity bez Play/bake (pravilo 2). Isprazni stari uvoz: samo FOLDERI u Assets osim Cinematic/Editor/Plugins/Scenes/Settings. **Nikad fajlovi u korenu** (URP GlobalSettings, DefaultVolumeProfile, InputSystem_Actions) — DeleteAssets na njima otvara modalni dijalog koji blokira MCP.
- Najnoviji importer: `python H:\UnrealToUnityExporter\pack_importer.py` → `Client.Add("file:L:/8TB/DEXSOFT Plugins/UnrealPlugins/UnrealToUnityExporterWithLandscape_1.0/UnrealToUnityExporterWithLandscape_1.0/UnityPackage/com.dexsoft.import-unreal-scene-1.0.0.tgz")`. `Client.Resolve()` NE povlači nov tgz sa iste putanje. Proveri string iz nove verzije u `Library/PackageCache/com.dexsoft.import-unreal-scene@*/...` i da `isCompiling == false`, konzola bez grešaka.
- Uvoz: `var r = Dexsoft.TerrainImport.UnrealTerrainBuilder.Build(@"H:\...\<P>\UnityExport");` — dugo traje, MCP vrati prazan odgovor; upiši `r.Warnings` u fajl i čekaj fajl. Ako se usred uvoza uđe u Play, pada na snimanju scene („cannot be used during play mode") → ponovi ceo uvoz posle izlaska iz Play.
- Scena se snima u `Assets/<Mapa>/<Mapa>.unity`. Uvoz radi i render setup (URP asset, lighting asset, post, sonde, APV) i self-contain na kraju.
- Posle uvoza: konzola bez grešaka, broj čestica/rotatora iz izveštaja, slike iz kamera (Camera.Render u RenderTexture → PNG) i poređenje sa Unrealom.

## 5. Bake (Dejan ga pokreće)
- Pre bake-a zatvori Unreal (VRAM). Ne diraj Unity dok traje.
- Proveri na disku: scena `m_LightingSettings` != 0, lighting asset `m_LightmapMaxSize: 4096`.
- Spoljni nivo sa terenom: objekti < 1 m i vegetacija bez Contribute GI, lokalni APV samo preko terena+modela, baking set 3/81 m.

## 6. Kopija u UnityExports
- `python H:\UnrealToUnityExporter\copy_to_unityexports.py <FolderNivoaUAssets> [Ime]` → robocopy Assets/Packages/ProjectSettings u `UnityExports\<Ime>`, prevezivanje referenci sa paketa na kopije u `Assets/<Nivo>/Source`, izbacivanje L: paketa iz manifest-a. Mora da ispiše `package refs left 0, L: paths left 0`.
- Kopija uzima ono što je NA DISKU. Izmena materijala se snima tek sa File → Save Project (Ctrl+S snima samo scenu) — pitaj Dejana pre kopije ako je štimovao.

## 7. Release (samo na odobrenje)
1. Build: `RunUAT.bat BuildPlugin -Plugin=H:\UnrealToUnityExporter\Plugins\UnrealToUnityExporterWithLandscape\UnrealToUnityExporterWithLandscape.uplugin -Package=H:\UTUB\UnrealToUnityExporterWithLandscape -TargetPlatforms=Win64 -Rocket` (RunUAT u `J:\EpicGamesDownloadFiles\UE_5.8\Engine\Build\BatchFiles\`).
2. Instalacija u engine (editori zatvoreni): `powershell -ExecutionPolicy Bypass -File H:\UnrealToUnityExporter\install_exporter_to_engine.ps1`.
3. `python H:\UnrealToUnityExporter\pack_importer.py` (tgz).
4. `python H:\UnrealToUnityExporter\release_zip.py` → zip `UnrealPlugin/UnrealToUnityExporterWithLandscape/{Binaries(dll+modules, bez pdb), Config, Source, uplugin}` + `UnityPackage/*.tgz` + `UserGuide.html/.md`, kopija u `SVIMCPSERVERI\DexsoftPlugins\Unreal`. Skripta proverava da DLL i tgz u zipu = build.
5. Dugme „Check latest UnityExporter" u editoru poredi MD5 8TB zipa sa `Resources/Installed.md5` i instalira.

## Gotovi paketi (UnityExports)
CityRacingTrack, MedievalCastle, MedievalHarbour, MedievalVillageMEGA, SpaceNightClub, WitchHouse (28.10.2026: noć, mesec, Niagara, kazan).
