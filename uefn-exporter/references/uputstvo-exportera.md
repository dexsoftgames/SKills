# Export To UEFN — guide for Claude in a new chat

Read this in full before any work on the exporter. After that, also read `H:\UnrealToUEFN\CLAUDE.md` (main rules
and the history of fixes) and `H:\UnrealToUEFN\UEFNExporterTest.md` (the test loop). This guide is the short map of
how it works and how to use it; the details are in those two files and in memory. State as of 29 Sep 2026.

## What it is

A plugin for **Unreal Engine 5.8**. In the level editor there is an **Export To UEFN** button: it takes the open level
and everything it uses, brings it within UEFN/Fab rules, and writes it into a **UEFN project** (Fortnite 42.20 / UEFN 6.0).
You open that project in UEFN and it runs: meshes, materials, lights, decals, Niagara effects, sounds, Blueprint logic
translated into Verse (turning fans, flickering lamps, monitors that change images).

It does not modify the source Unreal project. It works on copies in a staging folder, then copies the result into the UEFN
project. The only UEFN files it touches, besides its own: the default floor (GridPlane, removed for large scenes and
put back for small ones), its own old sound devices (tag `UEFNExportSound`), and the `bEnableToolsetsForProject` flag in
`.uefnproject`.

## Where things are

| What | Where |
|---|---|
| Plugin source (change ONLY here) | `H:\UnrealToUEFN\Plugin\UnrealToUEFN\Source\UnrealToUEFN\Private\` |
| Build | `H:\UnrealToUEFN\BuildPlugin.ps1` → `H:\UnrealToUEFN\PluginBuild\UnrealToUEFN` |
| In the engine (junction) | `J:\EpicGamesDownloadFiles\UE_5.8\Engine\Plugins\Marketplace\UnrealToUEFN` → PluginBuild |
| Source Unreal test projects | `H:\UnrealToUEFN\UnrealProjects\Test2..Test10`, `CoffeeHouseTest` |
| UEFN projects | `H:\UnrealToUEFN\UEFN\<Project>\` |
| Report of each export | `H:\UnrealToUEFN\UnrealProjects\<TestN>\Saved\UEFNExport\<Mount>\` |
| Helper scripts | `H:\UnrealToUEFN\Docs\` (uefn_mcp.py, screen.ps1, uefn_session.ps1, close_window.ps1) |
| Setting up a new computer | `H:\UnrealToUEFN\Docs\SETUP_NOVI_KOMPJUTER.md` + `.ps1` |

### Code map (`Private\`)

| File | What it does |
|---|---|
| `UEFNExport.cpp` | `Run()`: the whole export in order; reading `.uefnproject` (`LoadUEFNProject`), copy paths (`BuildDestinations`), `CopyPackages`, `Deploy`, default floor, summary window + Report.txt |
| `UEFNLevel.cpp` | `ScanLevel`: walks the level (what goes, what stays out and why), Blueprints taken apart into meshes/lights, spawn = middle of the largest room (`FindLargestRoomMiddle`), exposure/lights, sounds (`FSoundPlacement`); `BuildActorsForUEFNMap`: writes actors as external actors of the UEFN map |
| `UEFNAssetRules.cpp` | Fixes on the copies: textures ≤2048, mips, 8-bit, no virtual textures, LODs, Nanite off, mesh >20k vertices → Simplify, custom HLSL nodes → built-in, broken materials, SoundCue: Attenuation node out (UEFN refuses it) |
| `UEFNBlueprintVerse.cpp` | Translates a Blueprint event graph into Verse, node by node |
| `UEFNVerse.cpp` | Writes `UEFNBehaviors.verse` + `UEFNExportAssets.verse` (handle classes for materials/meshes) |
| `UEFNEffects.cpp` | Cascade → Niagara (Epic's converter, on a copy under `/UEFNConverted/`); `Sounds.json`; `StartSoundPlacement` (starts the sound helper) |
| `UEFNIcon.cpp` | `Resources\Icon128.png` = a picture of the level from the spawn point |
| `UEFNCollision.cpp` | Simple Collision Maker (right-click a mesh) |
| `UEFNReport.cpp` | Report (Error / Warning / Fixed / Info by rule) |
| `Resources\PlaceSounds.py` | Helper: waits for UEFN to open the project, then places Audio Player devices through the UEFN MCP |

## How to do an export (the order is mandatory)

### A. A new UEFN project (once per pack)
1. **Name = the name of the pack folder in `Content\` of the Unreal project** (Test10 → `AbandonedHospital`). Never TestN.
2. UEFN → New Project → Island Templates → **Blank** (NEVER Simple: it has its own ocean, island, and spawn pads at 3.84 m, so the scene
   sinks and the player lands on the roof). Location `H:\UnrealToUEFN\UEFN`.
3. In the Content Browser: + Add → New Folder `Maps`, drag the empty map into it (Move Here, OK on the warning).
   Right-click the root → Update Redirector References → Delete Unreferenced Redirectors. File → Exit.
4. Result: `UEFN\<Project>\Content\Maps\<Project>.umap`. The project name appears **only once**; no doubled folder.

### B. The export
1. **UE 5.8 and UEFN must never run at the same time** (the GPU crashes). `tasklist` before starting either.
2. Start UE:
   ```
   J:\EpicGamesDownloadFiles\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe "H:\UnrealToUEFN\UnrealProjects\TestN\TestN.uproject" -ini:Engine:[/Script/Engine.RendererSettings]:r.Shadow.Virtual.Enable=0 -ini:Engine:[SystemSettings]:r.Shadow.Virtual.Enable=0
   ```
   Wait for `Total Editor Startup Time` in `Saved\Logs\TestN.log`. ue-mcp: `project(set_project, projectPath=...)`.
3. `editor(set_dialog_policy, pattern="Export To UEFN", response="ok")`: otherwise the summary window blocks the bridge.
4. `editor(execute_command, command="ExportToUEFN H:/UnrealToUEFN/UEFN/<Project>")`. The bridge times out after 30 s;
   that is normal. Wait until `Saved\UEFNExport\<Mount>\Report.txt` changes. Check `0 errors`.
5. Close UE: `Stop-Process -Name UnrealEditor -Force` (the export leaves nothing unsaved; say so to Dejan).

### C. In UEFN
1. Open: `UnrealEditorFortnite-Win64-Shipping.exe "H:/UnrealToUEFN/UEFN/<Project>/<Project>.uefnproject"`, then
   double-click the tile in the picker (with `screen.ps1`, coordinates ×2).
2. **Sounds place themselves**: `SoundsPlaced.log` ends with `done: N of N`.
3. **The Verse device** (flickering lights, monitors, fans) must be placed once. First compile Verse through the MCP
   (`VerseToolset.BuildAll`), then `DeviceToolset.ListDeviceAssets` → the asset `.../_Verse.<module>-uefn_export_behaviors_device`
   → `PlaceDevice` + `SceneTools.save_actor`.
4. The spawn pads must be at the middle of the largest room (0, 0, ~2) (with Blank they already are).
5. Launch Session: `SessionToolset.StartSession` through the MCP + `uefn_session.ps1` in the background (it clicks
   "Make Private"). The log line `FlowStep_RunLocalValidation(): Complete` means validation passed.
   `Disallowed reference to ...` means an error; fix it in the exporter, never by hand in UEFN.

## Rules the exporter follows (approved by Dejan)

- Textures ≤2048; meshes ≤20,000 vertices (Test8 stays at 30k); materials ideally ≤500 pixel instructions.
- **Glass**: the heavy shaders (Thin Translucent + SceneColor) are invisible in UEFN. `M_Glass_Simple` in Test10 is APPROVED
  (Translucent, Volumetric Directional, 485 instructions, Frost 0.2, Refraction 1.05). Details are in CLAUDE.md.
- **Panel glass** (`M_Glass_Panels_NM`, the same in every pack): ALWAYS rebuilt on the copy as the simple glass
  (`SimplifyPanelGlass`: 10 nodes, Surface ForwardShading, same parameters). Recognised by structure, not by name.
  APPROVED 29.9.2026 on ModernOffice ("pa isto"). Other glass masters are left alone.
- **Sounds**: UEFN has no AmbientSound, only the Audio Player device. **Distances in UEFN are in METERS**, and Unreal gives cm
  (divide by 100). A 3D sound takes its range from Unreal. **A 2D sound becomes 3D with 20 m of full volume + 5 m falloff**. All sounds loop.
  A SoundCue must not contain an Attenuation node (it is removed, and its range moves into the cue's Attenuation Settings).
- Cascade → Niagara through Epic's converter; a system that uses `SpriteLockAxis` is left out (UEFN refuses its enum).
  The converter leaves InitializeParticle's Sprite Size at Niagara's 10 cm default: the exporter writes the Cascade start size
  (constant or uniform) into the spawn script (`CarryCascadeSpriteSizes`, `Effect.SpriteSize`), and compiles the system before
  saving it. OPEN (30.9.2026): the ControlRoom steam (PS_Steam_A, M_Smoke_Ground_C: translucent lit, alpha from a converted
  curve, DepthFade) is placed and validated but still not visible in the session.
- **Slide-show atlases (monitors)**: an atlas sampler whose UV goes through a Floor (cell by index) and whose source is 4096 is
  split into four 2048 quadrants at full resolution (`<T>_Q0..Q3`, `Texture.AtlasSplit`); the material reads them as parameters
  `<Param>_Q0..Q3` (mips from the continuous UV, no seam). An instance that puts its own 4096 atlas on that parameter gets that
  atlas's quadrants, and Verse replays them on the root class. Dejan 29.9.2026: "ako ima tako velikih atlasa da se dele uvek".
  An atlas read by a plain UV offset (ModernHospital, 1024x512 per slide) keeps one 2048 texture (approved).
- Lights are scaled to UEFN exposure (EV 2); lights driven by a Blueprint (flicker) are made by Verse as Scene Graph lights.
- The level is moved so that the middle of its largest room lands at the map's centre, 2 cm above the floor. UEFN's default floor is
  removed only for scenes larger than 100 m.
- Folders: `<Project>/Maps/<Project>` for the map, and the rest as in the Unreal pack (Meshes, Material, Texture, Sounds,
  Effects, Misc). Only UEFN Fab rules apply (not Unreal ones!): English/digits/`_`, no empty folders, path ≤140 characters,
  no redirectors, no `.py`.

## UEFN MCP (port 8001): what to know

- Client: `python H:\UnrealToUEFN\Docs\uefn_mcp.py call call_tool '{"toolset_name":...,"tool_name":...,"arguments":{...}}'`
  or import `Resources\PlaceSounds.py` (`Mcp` class) from Python.
- `SceneTools.find_actors` **requires** `collision_channels: []`. `ActorTools.set_actor_transform` takes `xform`, not
  `transform`. `ObjectTools.set_properties` takes `values` as a **JSON string**. Property names are display names
  (`"attenuation Min Distance"`, `"enable Spatialization"`, `"loopAudio"`...).
- There is no tool for deleting actors. The exporter deletes its devices' files while UEFN is closed.
- A UEFN project **cannot be deleted** from Epic's servers (only Archive), and its Verse path stays taken.
- `AssetTools.move` refuses to move the open map. Move it by hand in the Content Browser.

## Pitfalls that have already broken something

- Never change a shading model through Python on an existing material: it gives a black material. Swap the reference instead.
  (On 29 Sep 2026 two glass masters were broken this way; they were replaced with M_Glass_Simple and deleted.)
- ue-mcp `query_components` with `where` on array fields (materials) finds nothing. Use a Python script (`run_python_file`).
- A PowerShell command containing `SendKeys("{ESC}")`, or `Remove-Item` together with `robocopy /E`, is blocked by permissions;
  work around it (mouse clicks, `Copy-Item`).
- UEFN catches keystrokes if Dejan types while the agent clicks. Say before clicking.
- `UEFN\Test2..Test10` are old projects (TestN name, map in the root). When re-exporting a pack, make a NEW project with
  the proper name (step A).

## What is open (29 Sep 2026)

1. Test2..Test9 → new UEFN projects with the Content folder name (CorporateBuilding, ControlRoom3, ControlRoom2,
   ControlRoom, RetroStudio2, Warehouse, NexusNewsStudio, BilliardClub) + export + validation.
2. Placing the Verse device should be automatic (like the sounds). It is still done by hand through the MCP.
3. The report writes "N names reduced to English letters" for every asset, even when no name changed (false count
   since the pack folder was dropped). Compare against `UnderProject(Source.Mid(6))` in `BuildDestinations`.
4. The icon (`UEFNIcon.cpp`) comes out too bright and bluish: give the capture manual exposure from `Scan.SourceEV100`.
5. `UEFNBehaviors.verse` now lands in the `Meshes` folder (the common folder of the parts), so the device is called
   `Meshes-uefn_export_behaviors_device`. It works; maybe move it to a `Verse` folder, but ask Dejan first.

## Working rules (from CLAUDE.md, briefly)

- Before any code change: find the callers, and say what else it affects and why it behaves as before. One request = one change.
- The exporter must not modify the source project (except when Dejan explicitly asks, as with the glass).
- Git only when Dejan says "submituj git". Never reset/force.
- Say when you close an editor. Click UEFN dialogs straight away; don't wait.
- After "odlicno izgleda", don't keep experimenting on the same thing. Write the approved values down in CLAUDE.md.
