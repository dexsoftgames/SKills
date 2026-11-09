# Mapa koda

## Exporter (Unreal C++) — `Plugins\UnrealToUnityExporterWithLandscape\Source\UnrealToUnityExporterWithLandscape\Private\`

| fajl | šta |
|---|---|
| `LandscapeUnityExporter.cpp` | glavni tok exporta (faze, SlowTask, Cancel), heightmap/weightmape, manifest.json (svi blokovi), pečenje stene iz nagiba, posejana trava |
| `SceneMeshExporter.cpp/.h` | scene meševi, materijali (ResolveSlot / ResolveSlotByName / ResolvePbrByRule / ResolveEmissive / ResolveLiquid), sky dome (IsSkyDome + ReadSkyDome), fog volume, rotatori, override materijali po SEKCIJAMA LOD0 |
| `MaterialGraphAnalyzer.cpp` | analiza grafa (Analyze → BaseColor/Emissive/Opacity izvori, PanSpeed, tiling) |
| `MasterMaterialFixer.cpp` | ispravke Dexsoft mastera pre exporta (po strukturi, idempotentno) |
| `LayerTextureExporter.cpp` | teksture slojeva terena, auto-materijal, maske sirovo (LoadAsRawBGRA8) |
| `NiagaraExporter.cpp/.h` | Niagara → opis sistema (moduli, krive, renderi, teksture čestica, flipbook ParticleSubUV) |
| `WaterExporter.cpp` | voda (SingleLayerWater shading model → waterBodies) |
| `LightExporter.cpp` | svetla, HDRI, sky light, environment |
| `DecalExporter.cpp` | dekali |
| `FoliageAssetExporter.cpp` | foliage tipovi |
| `SplineMeshBaker.cpp` | pečenje splajnova (PropagateSplineDeformationToMesh) u prostor aktera |
| `ExportDedup.cpp` | spajanje identičnih tekstura/materijala + druga provera |
| `ExportImageUtils.cpp/.h` | WriteTextureAsPNG/TGA, LoadAsBGRA8/LoadAsRawBGRA8, TextureFileStem |
| `GrassProbe.cpp` | sonda gustine trave |
| `UnrealToUnityExporterWithLandscapeModule.cpp` | dugmad „Export Scene To Unity" i „Check latest UnityExporter" (MD5 vs Resources/Installed.md5, PowerShell update skripta čeka da se editori zatvore) |

Build.cs zavisi od Niagara, NiagaraCore, NiagaraEditor. `.uplugin` ima Niagara plugin zavisnost.
`UNiagaraNodeInput::GetDataInterface` nije exportovan (LNK2019) → čitati DataInterface preko refleksije.

## Importer (Unity) — `Plugins\com.dexsoft.import-unreal-scene\`

| fajl (Editor/) | šta |
|---|---|
| `UnrealTerrainBuilder.cs` | `Build(exportDir)` — glavni tok uvoza, redosled svih placera, snimanje posle render setupa (SaveAfterRenderSetup + UnrealSelfContain) |
| `UnrealManifest.cs` | klase za JsonUtility (JsonUtility NIKAD ne ostavlja ugnježden objekat null — „prazno" proveri po polju) |
| `UnrealJson.cs` | sopstveni JSON parser za delove koje JsonUtility ne ume (particles) |
| `UnrealScenePlacer.cs` | props, materijali (BuildMaterial, BuildLiquid, SaveMaterial = upis preko postojećeg), pečeni splajnovi |
| `UnrealModelMaterials.cs`, `UnrealModelPostprocessor.cs` | FBX materijali preko importer Remap-a |
| `UnrealFoliagePlacer.cs`, `UnrealWindPlacer.cs` | foliage, vetar, IsLeafSlot (alfa odlučuje) |
| `UnrealWaterPlacer.cs` | voda: preset + ApplyMeasuredColour + shore mapa |
| `UnrealSkyPlacer.cs` | HDRI ili Unrealova kupola (PlaceDome + Night* konstante) |
| `UnrealParticlePlacer.cs` | Niagara → Particle System prefabovi, grupa „Particles" (briše svoje stare instance) |
| `UnrealRotatorPlacer.cs` | RotatingMovement akteri → pivot `<ime>_Rotator` + DexsoftRotator |
| `UnrealLightPlacer.cs`, `UnrealRealtimeLighting.cs`, `UnrealRenderSetup.cs`, `UnrealEnvironmentPlacer.cs` | svetla, nebo/ambijent/magla, URP asset, post, sonde, APV, lighting asset |
| `UnrealFogPlacer.cs` | visinska i lokalna volumetrijska magla |
| `UnrealDecalPlacer.cs`, `UnrealLodTransitions.cs`, `UnrealRoomFinder.cs` (automatske sobe ISKLJUČENE) |
| `UnrealCameraPlacer.cs` | kamera + FlyCamera (Speed UVEK 1, FOV 90) |
| `UnrealImportPaths.cs`, `UnrealImportScene.cs`, `UnrealSelfContain.cs` | putanje (Assets/<P>/...), grupe u sceni, kopiranje paketnih fajlova u projekat + prepis GUID-ova |
| `DexsoftRenderSettings.cs`, `UnrealTerrainImportWindow.cs`, `DexsoftGlassGUI.cs` | meni Tools/Dexsoft/... |

Runtime/: `FlyCamera`, `DexsoftUvDrift` (MaterialPropertyBlock, bez kopija materijala), `DexsoftRotator` (samo Play), `DexsoftVolumetricFog(+Feature)`, `DexsoftFogVolume`, `WindZoneLink`, `AmbientRefresh`.
Šejderi (Runtime/Shaders): `DexsoftPanningCloudSky` (noćno nebo), `DexsoftAnimatedLiquid` (kazan), `UnrealSky` (dnevno, Dexsoft/Sky), `UnityWater`/`UnrealWater`, `DexsoftGlass`, `DexsoftRock`, `DexsoftStylizedMoss`, `FoliageCutout`, `UnrealFoliageWind`, `UnrealLitOverlay`, `DexsoftVolumetricFog`, `DecalWet.shadergraph`.
Preseti (Runtime/Materials): `M_DexsoftGlass/Lake/Ocean/Rock/Sky.mat`.

## Manifest (`UnityExport/manifest.json`) — glavni blokovi
`terrain`, `layers`, `foliage`, `sceneMeshes` (materials po slotu: baseColor, maps, metallic/smoothness, emissionColor, uvDrift, liquid{...}, glass...), `sceneInstances`, `overrideMaterials`, `waterBodies`, `decals`, `lights`, `reflectionProbes`, `environment` (heightFog, manualExposure, localPostProcess...), `sky` (HDRI), `skyDome`, `particles` {systems[emitters[modules, renderers]], placements}, `rotators`, `fogVolumes`, `wind`, `source`.
Sve pozicije u manifestu su već u Unity prostoru: metri, Unity(x,y,z) = Unreal(Y,Z,X)*0.01; kvaternion (Q.Y, Q.Z, Q.X, Q.W). Izuzetak: `skyDome.lightDirection` je u Unreal osama (šejder radi u Unreal osama).
FBX: bakeAxisConversion + yaw −90° na detetu (NIKAD mirror scale −1).

## Trajne skripte (`H:\UnrealToUnityExporter\`, kopije u `scripts/`)
- `pack_importer.py` — importer tgz na 8TB UnityPackage (odbija < 50 fajlova).
- `install_exporter_to_engine.ps1` — H:\UTUB build → engine Marketplace (bez .pdb, EnabledByDefault). Odbija ako radi editor.
- `copy_to_unityexports.py <Nivo> [Ime]` — nezavisna kopija Unity projekta.
- `release_zip.py` — release zip + SVIMCPSERVERI kopija + provere.
