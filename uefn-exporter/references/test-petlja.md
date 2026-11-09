# UEFNExporterTest — predaja za novi chat (28.9.2026)

Dejan je rekao (28.9.2026): „u drugom chatu povezao sam se sa mobilnim ... nastavljamo sa testom svih
foldera da exportujemo sve pakete" i „ajde da upalimo remote da mozes sam da radis a ja da pratim".
Znaci: radis SAM, bez cekanja na njegove klikove; on samo prati.

Dejan radi REMOTE sa mobilnog: ti sve radis sam (izvoz, otvaranje UEFN-a, klikovi), on prati.
Pisi mu na srpskom, kratko. Prvo procitaj `H:\UnrealToUEFN\CLAUDE.md` (pravila i utvrdjene cinjenice).

## Cilj sada
Test svih foldera: redom izvesti sve pakete (Test2..Test10) u njihove UEFN projekte, otvoriti svaki
u UEFN-u, pokrenuti Launch Session, procitati greske iz loga, popraviti u pluginu, ponoviti.
Popravke SAMO u deljenom pluginu `H:\UnrealToUEFN\Plugin\UnrealToUEFN\Source\UnrealToUEFN\Private\`.

## Stanje (sta radi, ODOBRENO od Dejana)
- Test3 (ControlRoom3): "odlicno je uspelo". Propeleri se vrte (Verse), monitori menjaju slike, dugmici
  trepere — sve preko PREVODA Blueprint grafa u Verse cvor po cvor (`UEFNBlueprintVerse.cpp`).
- Svetla EV 2 (cvar UEFNExport.LightTargetEV), scena na centru mape na betonskom podu (mala scena),
  UEFN pod se brise samo za scene > 100 m, dekali ispravno rotirani, spiralne ograde 3 stepenika/box.
- Test2 (CorporateBuilding) stoji sa strane: 21 Text3D natpis, odluka Dejanova (obrisati ili pretvoriti u mesh).
  Text3D je jos ukljucen u Test2.uproject.

## Nov UEFN projekat (od 29.9.2026, GLAVNA PRAVILA u CLAUDE.md)
1. Ime = ime foldera paketa u `Content\` Unreal projekta (Test10 → AbandonedHospital). Nikad TestN.
2. UEFN: File → New/Open Project → Island Templates → **Blank** (NIKAD Simple: ima svoje ostrvo, okean i
   planine pa scena potone u njih — AbandonedHospital 29.9.), lokacija `H:\UnrealToUEFN\UEFN`, ime, Create.
3. U Content Browseru: + Add → New Folder `<Ime>`, u njemu `Maps`; prazna mapa `<Ime>` se prevuce u
   `<Ime>/Maps` (Move Here, OK na upozorenje). Desni klik na koren → Update Redirector References →
   Delete Unreferenced Redirectors. Prazan folder se brise. Izlaz: File → Exit (ne CloseMainWindow).
4. Izvoz u `H:/UnrealToUEFN/UEFN/<Ime>` → exporter nadje mapu u `<Ime>/Maps`, upali MCP u .uefnproject
   i pokrene helper za zvuk.
5. Otvori projekat (My Projects, proveri Project File desno). Helper postavi zvuke sam.
   `uefn_export_behaviors_device` se jednom postavi preko MCP PlaceDevice
   (`/<Ime>/_Verse.<Ime>-uefn_export_behaviors_device`) + save_actor.
6. Launch Session preko MCP `SessionToolset.StartSession` + `uefn_session.ps1` za „Make Private".
Stari `UEFN\Test2..Test10` ostaju dok Dejan ne kaze da se brisu.

## Kako se radi jedan test (redosled je obavezan)
1. UEFN i UE 5.8 NIKAD zajedno (pad GPU-a). `tasklist` proveri pre svakog pokretanja.
2. Pokreni UE editor projekta (Test3 pada na startu u virtuelnim senkama, pa uvek ovako):
   `J:\EpicGamesDownloadFiles\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe "H:\UnrealToUEFN\UnrealProjects\TestN\TestN.uproject" -ini:Engine:[/Script/Engine.RendererSettings]:r.Shadow.Virtual.Enable=0 -ini:Engine:[SystemSettings]:r.Shadow.Virtual.Enable=0`
   Cekaj u `Saved\Logs\TestN.log` red `Total Editor Startup Time`. Bridge: ue-mcp `project(get_status)`.
3. Izvoz: `editor(execute_command, "ExportToUEFN H:/UnrealToUEFN/UEFN/TestN")` (`-nodeploy` = samo staging za proveru).
   Izvestaj: `H:\UnrealToUEFN\UnrealProjects\TestN\Saved\UEFNExport\TestN\Report.txt`.
   Posle izvoza iskace modalni prozor sa sazetkom (samo OK) i blokira bridge — ugasi UE procesom
   (`Stop-Process UnrealEditor`), izvoz nista ne ostavlja nesacuvano.
4. Verse provera pre UEFN-a: `scratchpad\verse_check_multi.py TestN 150 <fajlovi .verse u UEFN projektu>`
   (verse-lsp; "no diagnostics received" = cisto; hvata i greske pristupa modulima).
5. UEFN: `"C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe" "H:/UnrealToUEFN/UEFN/TestN/TestN.uefnproject"`
   Cekaj u `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Logs\UnrealEditorFortnite.log` red
   `Total Editor Startup Time`, pa `scratchpad\screen.ps1` (screenshot u pola rezolucije, koordinate x2),
   pa `screen.ps1 -ClickX X -ClickY Y -Double` na plocicu projekta. Otvoreno kad log kaze
   `OpenProject_FinalizeAndLoadMap - Done`; Verse build: `VerseBuild: SUCCESS`.
6. Uredjaj `uefn_export_behaviors_device` mora jednom biti u mapi (Test3 ga ima). Ako ga nema, Dejan ga
   prevuce iz Content Browsera (ili UEFN MCP Creative Devices).
7. Launch Session: klik na dugme u toolbaru (Test3: pola-slika ~(366,38) → (732,77)). Log:
   `FlowStep_RunLocalValidation(): Complete` = validacija prosla; klijent `FortniteClient-Win64-Shipping`;
   log klijenta `%LOCALAPPDATA%\FortniteGame\Saved\Logs\FortniteGame.log`.
8. Build plugina: sve UE 5.8 zatvoriti, `& "H:\UnrealToUEFN\BuildPlugin.ps1"` (UEFN sme da ostane otvoren).

## Blueprint → Verse (novo, 28.9.2026)
- `UEFNBlueprintVerse.cpp` (TranslateBlueprints, poziva se odmah posle ScanLevel): graf → Verse klasa
  `uefn_bp_<BP>`; nepoznat cvor = Warning `Blueprint.Logic` sa imenom cvora, akteri ostaju staticni.
- `UEFNVerse.cpp` (WriteVerseBehaviours): `<Pack>/UEFNBehaviors.verse` + `UEFNExportAssets.verse` u
  folderima asseta (handle klase za materijal/mesh/teksturu, jer su folder moduli interni i
  material se ne moze cast-ovati). Cita UEFN digest da zna koje parametre/slotove klasa ima.
- Podrzano: BeginPlay, custom eventi, Delay, Set Timer by Event/Clear, Branch, Sequence, math/random,
  Create Dynamic Material Instance, Set Scalar/Vector/Texture Parameter, Set Material, promenljive.
  Nije jos: Tick, Timeline, makroi (ForLoop), svetla iz grafa, cast na druge aktere.
- Verse zamke: podrazumevana vrednost polja ne sme pozivati funkciju; ime `Max` itd. se sudara sa
  Verse funkcijama; boje su ACES 2065-1 (konverzija iz radnog prostora u kodu).

## Otvoreno
- Para (Cascade P_Steam_A3) se ne prenosi — Dejan odlucuje (Niagara zamena ili bez).
- Test2 Text3D odluka. Zatim Test4..Test10 redom.
- U CLAUDE.md upisati odobreni Blueprint→Verse prevod (Test3 odobren "odlicno je uspelo").

## Pravila (ukratko, detalji u CLAUDE.md i memoriji)
- Exporter NE SME da menja izvornu Unreal scenu. Git samo citanje. Export/uvoz samo uz odobrenje
  (za ovaj test svih foldera Dejan je odobrio izvoz svih paketa).
- Pre svake izmene koda: pozivaoci, sta se jos menja; posle izmene reci sta je dirnuto i zasto je bezbedno.
- Menjaj samo trazeno; posle "odlicno" ne eksperimentisi dalje na istom.
- Reci kad zatvaras editor. Standalone uvek fullscreen.

## Stanje 28.9.2026 23:35 (kraj dana)
- Test2..Test10 izvezeni i pusteni u UEFN (Launch Session, Game Mode), svi 0 gresaka. Snimci: `Docs\Screens\`.
- Sve novo je opisano u CLAUDE.md (odeljak „Stanje 28.9.2026 uvece").
- OTVORENO za sledeci put:
  1. ~~Zvuk~~ URADJENO 29.9.: exporter sam postavlja Audio Player uredjaje (helper `Resources\PlaceSounds.py` ceka
     da UEFN otvori projekat; log `SoundsPlaced.log`). Detalji u CLAUDE.md „Zvuk (29.9.2026, AUTOMATSKI)".
  2. Niagara: sistem sa `SpriteLockAxis` (konverterov enum) se izostavlja; Test10 P_? efekat fali (Report: Effect.LeftOut).
  3. Test2 Text3D odluka, para u Test3 (Cascade) sada moze kroz konverziju — ponovo izvesti Test3/4/5/10 da dobiju Niagaru.
  4. Test8 ostao na granici 30k verteksa (Dejan), ostali od Test9 na 20k.
- Skripte za UEFN klikove: `scratchpad\uefn_session.ps1` (Launch Session + klik „Make Private"), `close_window.ps1`.
  (skripte su kopirane u H:\UnrealToUEFN\Docs\: uefn_session.ps1, close_window.ps1, screen.ps1)
