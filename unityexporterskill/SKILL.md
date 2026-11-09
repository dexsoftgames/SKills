---
name: unityexporterskill
description: Sve o Dexsoft exporteru „Export Scene To Unity" (Unreal 5.8 → Unity 6 URP, plugin UnrealToUnityExporterWithLandscape + Unity paket com.dexsoft.import-unreal-scene) - kako radi, gde je kod, build/instalacija/pakovanje, postupak po Fab paketu, odobrene vrednosti (materijali, svetlo, voda, vegetacija, nebo, čestice) i zamke koje su već nešto pokvarile. Koristi kad Dejan pomene Unity export/import, UnityExporter, „Check latest UnityExporter", Fab paket za Unity, UnityExports kopiju, manifest.json, importer, bake u Unity-ju, ili kad treba menjati/graditi/pakovati exporter ili importer.
---

# Unity exporter (Unreal → Unity) — Dejanova pravila i znanje

Odgovaraj UVEK na srpskom. Sve vrednosti označene kao ODOBRENO je Dejan potvrdio okom — ne menjati bez njegovog traženja.
Detalji su u `references/` (čitaj onaj koji se tiče posla):

| fajl | šta |
|---|---|
| `references/tok-rada.md` | ceo krug: Fab paket → UE projekat → export → Unity uvoz → UnityExports kopija → release na 8TB |
| `references/kod-mapa.md` | gde je koji deo koda (exporter .cpp, importer .cs, šejderi), manifest blokovi, build/instalacija |
| `references/materijali.md` | PBR/ARM/MetallicSmoothness, teksture T_/TGA, duplikati, emisija, tečnost, UV drift, staklo |
| `references/svetlo-render.md` | render setup, ekspozicija, APV bake, sobe/lokalni PP, sonde, magla, kamera, dnevno nebo |
| `references/nebo-cestice-voda-vegetacija.md` | noćno nebo (odobrene vrednosti), Niagara→Particle System, rotatori, voda, vetar, foliage |
| `references/zamke.md` | sve što je već jednom pokvarilo nešto, sa datumom i uzrokom |
| `references/novi-racunar.md` | šta treba na drugom računaru, putanje, MCP, instaler |
| `scripts/` | kopije trajnih skripti iz `H:\UnrealToUnityExporter\` (pack_importer, copy_to_unityexports, install_exporter_to_engine, release_zip) |

## Gde je šta (glavni računar)

- Izvor exportera (Unreal C++): `H:\UnrealToUnityExporter\Plugins\UnrealToUnityExporterWithLandscape`
- Izvor importera (Unity): `H:\UnrealToUnityExporter\Plugins\com.dexsoft.import-unreal-scene`
- Instaliran exporter: `J:\EpicGamesDownloadFiles\UE_5.8\Engine\Plugins\Marketplace\UnrealToUnityExporterWithLandscape` (EnabledByDefault, NIKAD `Engine\Plugins\Dexsoft`)
- Build izlaz: `H:\UTUB\UnrealToUnityExporterWithLandscape` (kratka putanja zbog 260 znakova)
- UE projekti paketa: `H:\UnrealToUnityExporter\UnrealProjects\<Ime>` (ime ≤ 20 znakova); export ide u `<Projekat>\UnityExport\`
- Radni Unity projekat: `H:\UnrealToUnityExporter\UnityProject` (vuče importer iz 8TB tgz-a)
- Gotove kopije: `H:\UnrealToUnityExporter\UnityExports\<Ime>`
- Release (posle odobrenja): `L:\8TB\DEXSOFT Plugins\UnrealPlugins\UnrealToUnityExporterWithLandscape_1.0\` (+ kopija zipa u `SVIMCPSERVERI\DexsoftPlugins\Unreal`)

## GLAVNA PRAVILA (svako je već jednom bilo prekršeno)

1. **Export TEK kad su šejderi gotovi.** Posle `level.load` čekaj da `editor(get_engine_state).compiling.shaders` i `.assets` budu 0 i da log miruje ~40 s. Export usred kompajliranja = pola modela (64 umesto 136).
2. **Ne diraj Unity dok radi bake ili Play.** Pre SVAKE izmene (Client.Add paketa, kopija šejdera, materijal, prefab, scena, uvoz) proveri `Lightmapping.isRunning || EditorApplication.isPlaying`. Ako je true — ne radi ništa, javi da čekaš. (28.10. pao Unity i izgubljen bake.)
3. **Pre bake-a zatvori Unreal** (VRAM) — inače GPU „device removed" / nvlddmkm.
4. **Reci kad zatvaraš Unreal editor** (zbog instalacije DLL-a). Zatvaranje: `editor(request_editor_shutdown, requireClean)` → sačekaj da proces nestane → instaliraj → `start_editor` → `level.load` mape.
5. **Pakovanje na 8TB (zip/release) TEK na Dejanovo odobrenje.** Importer tgz se pravi `pack_importer.py` (piše u 8TB UnityPackage folder) da bi Unity mogao da ga učita — to je radna kopija; zip za dugme „Check latest" tek kad on kaže.
6. **Novi fajl u importer paketu MORA imati .meta** (tgz je immutable; bez .meta Unity ga ignoriše). Posle pakovanja `Client.Add("file:...tgz")` i proveri string u `Library/PackageCache/com.dexsoft.import-unreal-scene@*`.
7. **Uvoz kopira šejdere/skripte u `Assets/<P>/Source/...`** (self-contain). Scena koristi TU kopiju — izmena šejdera samo u paketu ne menja otvorenu scenu dok se kopija ne prepiše ili uvoz ponovi.
8. **Prepoznavanje po STRUKTURI grafa, ne po imenima.** Nova izmena ne sme da pokvari paket koji je ranije prolazio (UnityExports su referenca).
9. **Teksture:** prefiks `T_` (nikad `MI_`), sve sa alfom = TGA, ARM se nikad ne preskače (uvek `T_<ime>_MetallicSmoothness.tga`), identične teksture/materijali = JEDAN fajl.
10. **Finalni Unity projekat je nezavisan:** sve u `Assets/<P>/...`, 0 referenci na paket, 0 L: putanja (`copy_to_unityexports.py` to proverava).
11. **Dejanove ručne vrednosti se ne pregaze.** Kad on nešto štimuje u Unity-ju, pre upisa u kod PITAJ da li je snimljeno (Save Project) i čitaj živo preko MCP-a, ne stari fajl sa diska. (28.10. dva puta upisano iz zastarelog fajla — „trčiš odma bez mozga".)
12. Posle svake izmene u poruci navedi šta je još dodirnuto i zašto je isto kao pre (CLAUDE.md pravilo).

## Brzi tok (detalji u references/tok-rada.md)

1. UE projekat paketa otvoren → mapa učitana → čekaj šejdere = 0.
2. Unity: isprazni prethodni uvoz (samo FOLDERE u Assets osim Cinematic/Editor/Plugins/Scenes/Settings), proveri da je učitan najnoviji importer.
3. `editor(execute_command, "ExportSceneToUnity")` → progres prozor je sam export; čekaj da se `UnityExport\manifest.json` osveži.
4. Proveri manifest (broj meševa, `particles`, `skyDome`, `liquid`, `rotators`, ...) i log (`Saved/Logs/<P>.log`, `LogExportToUnity`).
5. Unity: `Dexsoft.TerrainImport.UnrealTerrainBuilder.Build(@"<P>\UnityExport")` (ili meni Tools/Dexsoft/Import Scene From Unreal With Landscape). Izveštaj = `r.Warnings`.
6. Slikaj iste delove u Unrealu i Unity-ju i uporedi (merilo uspeha, ne broj objekata).
7. Kad Dejan kaže da je dobro: `python H:\UnrealToUnityExporter\copy_to_unityexports.py <Mapa> <Ime>` → `UnityExports\<Ime>`.
8. Na odobrenje: `python H:\UnrealToUnityExporter\release_zip.py` (zip + SVIMCPSERVERI kopija).
