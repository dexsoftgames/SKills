---
name: uefn-exporter
description: Sve o Dexsoft exporteru „Export To UEFN" (Unreal 5.8 → UEFN/Fortnite): kako radi, gde je kod, build i instalacija, postupak po Fab paketu, provere posle izvoza, teren, spawn, zvuk, Verse, staklo i sve zamke koje su vec nesto pokvarile. Koristi kad Dejan pomene UEFN, Fortnite, „Export To UEFN", „Update UEFN Exporter", izvoz paketa u UEFN, Fab pakete za UEFN, Launch Session, ili kad treba menjati/graditi/pakovati UnrealToUEFN plugin.
---

# Export To UEFN — Dejanov exporter (Unreal 5.8 → UEFN)

Odgovaraj UVEK na srpskom, kratko. Sva pravila ovde su ODOBRENA od Dejana (datumi u referencama).
Vrednosti se ne menjaju bez traženja. Kad Dejan kaže „odlično", ne eksperimentiši dalje na istom.

## Šta je

Engine plugin za **UE 5.8**. Dugme **Export To UEFN** (i **Update UEFN Exporter**) na toolbaru svakog projekta.
Uzme otvoreni nivo i sve što koristi, NA KOPIJI ga uskladi sa UEFN/Fab pravilima i upiše u **UEFN projekat**
(meševi, materijali, svetla, dekali, Niagara, zvuk, teren, Blueprint logika → Verse). Izvor se NIKAD ne menja.
Konzola: `ExportToUEFN <folder UEFN projekta> [-analyze] [-nodeploy] [-only=/Game/..]`.

## Gde je šta (Dejanov glavni računar; na drugom proveri diskove)

| Šta | Gde |
|---|---|
| Izvor koda (menja se SAMO ovde) | `H:\UnrealToUEFN\Plugin\UnrealToUEFN\Source\UnrealToUEFN\Private\` |
| Build | `H:\UnrealToUEFN\BuildPlugin.ps1` → `H:\UnrealToUEFN\PluginBuild\UnrealToUEFN` |
| U engine-u | `<UE_5.8>\Engine\Plugins\Marketplace\UnrealToUEFN` — **NIKAD `Engine\Plugins\Dexsoft`** (28.10.2026: van Marketplace pada SVAKI C++ build) |
| Gotov plugin (glavna kopija) | `L:\8TB\DEXSOFT Plugins\UnrealPlugins\UnrealToUEFN_UE5.8_Win64\` (zip + raspakovano + `Install.bat`/`Install.ps1`) |
| Instaler za nov računar | `L:\8TB\DEXSOFT Plugins\SVIMCPSERVERI\` (Setup.ps1, kopija plugina u `DexsoftPlugins\Unreal`, skill u `Claude\skills`) |
| UE 5.8 | `J:\EpicGamesDownloadFiles\UE_5.8\` |
| UEFN | `C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe` |
| Izvorni UE projekti / UEFN projekti | `H:\UnrealToUEFN\UnrealProjects\<Ime>` / `H:\UnrealToUEFN\UEFN\<FolderPaketa>` |
| Izveštaj izvoza | `<UE projekat>\Saved\UEFNExport\<Mount>\Report.txt` (+ .json, manifest.json, Sounds.json, SoundsPlaced.log) |
| Pomoćne skripte | `scripts\` ovog skilla; original `H:\UnrealToUEFN\Docs\` i `Docs\FabUcitavanje\` |
| UEFN log | `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log` |

Mapa koda: `UEFNExport.cpp` (tok `Run()`, kopiranje, deploy, sažetak), `UEFNLevel.cpp` (skeniranje nivoa, spawn,
tlo, teren, akteri kao external actors), `UEFNAssetRules.cpp` (teksture, meševi, LOD-ovi, materijali, staklo),
`UEFNBlueprintVerse.cpp` + `UEFNVerse.cpp` (BP → Verse), `UEFNEffects.cpp` (Cascade→Niagara, zvuk),
`UEFNIcon.cpp`, `UEFNReport.cpp`, `UnrealToUEFNModule.cpp` (dugmad, Update), `Resources\PlaceSounds.py` (zvuk u UEFN-u).

## GLAVNA PRAVILA (ne kršiti)

1. **UE 5.8 i UEFN NIKAD istovremeno** (pada GPU). `tasklist` pre pokretanja bilo kog. Reci kad zatvaraš editor.
2. **Ime UEFN projekta = ime foldera paketa u `Content\`** (Test10 → `AbandonedHospital`), nikad ime UE projekta.
3. **UEFN projekat iz šablona Blank** (nikad Simple). Glavna mapa UVEK `Content\Maps\<Projekat>.umap`; ime projekta
   samo jednom; ostali folderi kao u paketu. Važe SAMO UEFN/Fab pravila, ne Unreal.
4. **Spawn platforme = PlayerStart paketa** (21.10.2026). Sredina najveće sobe samo kad nema PlayerStart-a.
5. **Visina = izmereno tlo** (`FindGroundHeight`, trace mreža), nivo stoji 2 cm iznad UEFN poda. Posle SVAKOG
   izvoza proveri `[Level.MapOffset]` i vizuelno da paket nije potonuo (20.10.2026 Prison je potonuo 6,7 m).
6. **Imena PRE izvoza** ispravljaš u IZVORU: pravopis i ne-engleska imena (`list_names.py` → `rename_by_name.py` →
   fixup redirectors → save). Folder `mesh` → `Meshes` (Verse tip). Ništa drugo ne preimenuj (MI_PlasticBlack ostaje).
7. **Poligoni**: pre izvoza `audit_meshes.py`; LOD0 > 30.000 trouglova ili > 20.000 verteksa exporter smanjuje
   GEOMETRIJU (`BakeSimplifyLOD0`), posle izvoza svaki sa spiska mora biti `Mesh.Simplified`. LOD-ovi 100/75/50 %.
8. **Teksture ≤ 2048**, granica po najvećem mešu koji je koristi; >1M teksela ne-pow2 → pow2; VT isključen na kopiji.
9. **Okruženje se ne prenosi** (sunce, sky light, nebo, magla, oblaci, PPV): UEFN ima svoje, Time of Day 3 PM.
   Lokalna svetla idu, skalirana na EV 2.
10. **Teren** (od 21.10.2026): Landscape se gradi u UEFN mapi iz visina i slojeva izvora (`BuildTerrainForUEFNMap`).
    Limit 2048×2048 verteksa; visibility sloj se NE uvozi (pad editora). Preko limita sad Error `Level.TerrainTooBig`.
11. **Pre izvoza sačekaj šejdere**: `editor(get_engine_state)` dok `compiling.shaders` i `.assets` nisu 0.
12. **Izvoz i uvoz se ne pokreću bez dogovora**; git samo na „submituj git"; jedan zahtev = jedna izmena;
    pre koda proveri pozivaoce i šta izmena može da pokvari.

## Postupak po paketu (Fab lista)

1. Nov UE projekat iz šablona `Docs\FabUcitavanje\ProjectTemplate` (`pack.ps1 -Step newue -Name X`), Fab → My Library
   → „+". Zapiši folder paketa i glavnu mapu (`Overview.umap` se ne izvozi). Detalji: `references/fab-paketi.md`.
2. U izvoru: imena (pravilo 6), `audit_meshes.py` (pravilo 7). Snimi.
3. UEFN: New Project → Blank → ime = folder paketa → `Maps` → prevuci mapu → Update Redirector References →
   Delete Unreferenced → File > Exit (sačekaj ~60 s posle New Project).
4. UE: otvori projekat SA MAPOM u komandnoj liniji
   (`UnrealEditor.exe "<.uproject>" /Game/<Paket>/Maps/<Mapa>`) — posle starta je inače „Untitled" i izvoz odbija.
   **Ne radi `load_level` iz Python-a preko mosta** (pad). Sačekaj šejdere.
5. `editor(set_dialog_policy, "Export To UEFN", ok)` (i `"Redirector Update Report"`), pa
   `editor(execute_command, "ExportToUEFN H:/UnrealToUEFN/UEFN/<Projekat>")`. Timeout mosta je normalan; kraj je u
   logu: `LogExportToUEFN: Display: ExportToUEFN: exported`. Pročitaj Report.txt.
6. Zatvori UE (`Stop-Process -Name UnrealEditor`; ako javi da je mapa dirty → Don't Save).
7. UEFN: pokreni exe sa `.uefnproject`, sačekaj `Total Editor Startup Time`, **screenshot pa dvoklik na pločicu PO
   IMENU** (prva pločica = poslednji otvoren projekat — dvaput je otvoren Prison umesto Blacksmith-a).
   Čekaj `OpenProject_FinalizeAndLoadMap - Done`.
8. Verse build (VERSE OK, bez grešaka u logu), Launch Session + `uefn_session.ps1` (klikne „Make Assets Private"
   do 30 puta), `FlowStep_RunLocalValidation(): Complete`. Prava igra počinje tek sa `EndGamePhase_ClientMetrics`.
9. Screenshot Dejanu. Sledeći paket tek kad on potvrdi (ili ako je rekao „radi sam do kraja").

Dok se čeka UEFN/UE: screenshot na 20–30 s i ODMAH klikni prozor koji iskoči (Make Private, Unable to Play → OK,
Validation Fix-up → Skip). Klikovi: `scripts\screen.ps1` (slika na pola veličine → koordinate ×2). Pre klikanja
reci Dejanu da ne dira računar; minimizuj ostale prozore (VS Code/Maya/Discord gutaju klikove).

## Provere posle SVAKOG izvoza (obavezno, ne zaboravljati)

- `Result: exported: 0 errors` (jedini dozvoljen izuzetak: `Source.Modified` posle terena — zatvori bez snimanja).
- `[Level.MapOffset]`: odakle je uzet spawn (PlayerStart!) i za koliko je pomeren; `[Level.GroundRule]` ako tlo nije
  najniži ravni meš. U UEFN-u pogledaj da paket stoji NA podu.
- `[Level.Terrain]` ako nivo ima Landscape (veličina, broj slojeva).
- Svaki meš iz `audit_meshes.py` je `Mesh.Simplified`.
- `SoundsPlaced.log` → `done: N of N`; Verse OK; validacija Complete.
- Bezopasno: 3× „Missing Preview connection for function input" (MF_TexCoordScale, MF_SelectTexCoord,
  MF_sampleScaledNormalMap); `Mesh.CollisionCount` (kolizija se pravi u izvoru alatom Simple Collision Maker).

## Build, instalacija, izdanje

- Build SAMO `BuildPlugin.ps1` (vraća `EnabledByDefault: true`); svi 5.8 editori zatvoreni (DLL zaključan).
- Posle builda: zip na 8TB (raspored: `UnrealToUEFN\` sa uplugin, `Binaries\Win64` dll+modules, `Resources\PlaceSounds.py`,
  `Source\`; plus `Install.ps1`, `README.txt`, `ClaudeSkill\uefn-exporter`), raspakuj pored zipa, osveži kopiju u
  `SVIMCPSERVERI\DexsoftPlugins\Unreal`.
- `Install.bat` (pored zipa): otpakuje zip, nađe UE 5.8 (registar, LauncherInstalled.dat, diskovi), prepiše plugin u
  engine i instalira ovaj skill u `%USERPROFILE%\.claude\skills\`. Na razvojnom računaru (junction) odbija bez `-ReplaceLink`.
- Dugme **Update UEFN Exporter**: MD5 zipa (zapamćena putanja ili 8TB; ako ga nema — Browse) vs
  `Resources\Installed.md5`; ako se razlikuje: Yes → editor se sam zatvori, skripta čeka sve `UnrealEditor` procese,
  pokrene `Install.ps1` iz zipa. Stara verzija nema dugme → jednom `Install.bat`.

## Reference (čitaj po potrebi)

- `references/uputstvo-exportera.md` — kratka mapa: kako radi, redosled, UEFN MCP zamke, otvoreno.
- `references/istorija-i-pravila.md` — CEO `H:\UnrealToUEFN\CLAUDE.md`: Fab zahtevi, svaka ispravka sa datumom
  (staklo, atlasi monitora, zvuk, Cascade, svetla po EV, kolizija, Simple Collision Maker, teren, spawn...).
- `references/uefn-fab-pravila.md` — tabela „sme / ne sme / uslovno" iz Epic dokumentacije sa izvorima.
- `references/fab-paketi.md` — liste paketa koje su urađene, koraci učitavanja sa Faba, zamke automatike.
- `references/test-petlja.md` — petlja testiranja na Test projektima.
- `references/novi-racunar.md` — postavka novog računara (programi, VS 2026 toolchain, MCP, plugin).
- `scripts/` — `uefn_mcp.py` (klijent za UEFN MCP 8001: `call call_tool '{"toolset_name":..,"tool_name":..,"arguments":{..}}'`),
  `uefn_session.ps1`, `screen.ps1`, `pack.ps1`, `wait.sh`, `audit_meshes.py`, `list_names.py`, `rename_by_name.py`.

UEFN MCP zamke: `find_actors` traži `collision_channels: []`; argumenti idu pod `"arguments"`; nema brisanja aktera;
UEFN projekat se ne može obrisati sa Epic servera (samo Archive). Python u UEFN-u je uključen po projektu.

## Otvoreno (stanje 9.11.2026)

- Teren veći od 2048×2048: predlog je prozor oko sadržaja paketa (seče se uz komponente), smanjivanje samo ako
  sadržaj ne staje — čeka Dejanovu potvrdu.
- `Source.Modified` posle izvoza terena (izvorna mapa ostane dirty).
- Kozmetika u `Level.MapOffset`: broj kolona tla prikazuje zbir tri bina.
- Para (Cascade steam) u ControlRoom paketima se ne vidi u sesiji.
