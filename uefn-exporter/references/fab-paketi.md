# Fab paketi → UEFN (istorija lista i naučene zamke)


Dejan 29.9.2026: `H:\UnrealToUEFN\UnrealProjects` je ispražnjen (stari Test2..Test10 više nisu tu). Novi tok po paketu sa Dejanove liste:
1. Prazan UE 5.8 projekat, ime = ime sa liste, u `UnrealProjects\<Ime>`.
2. Fab dugme u editoru (vezano za Dejanov nalog) → My Library → paket → Add to Project.
3. `Plugins\UE_MCP_Bridge` kao junction na deljeni `H:\UnrealToUEFN\Plugin\UE_MCP_Bridge` (exporter je engine plugin, sam se vidi).
4. Nov UEFN projekat iz **Blank** šablona, isto ime, u `H:\UnrealToUEFN\UEFN`, pa ExportToUEFN u njega.
5. UEFN: prvo build Verse, pa Launch Session, pregled grešaka, screenshot Dejanu.
6. Tek na Dejanovu potvrdu sledeći paket. Ono što exporter ne zna dopisuje se u exporter (plugin izvor).

Stanje 29.9.2026: ModernOffice (Unreal `ModernOffices`, folder paketa `ModernOffice`) izvezen, 0 grešaka, sesija radi; exporter od tada UVEK menja panel staklo jednostavnim (detalji u H:\UnrealToUEFN\CLAUDE.md). Paketi su Lumen — ne tražiti uzrok mraka u pečenom svetlu. ModernOffice ODOBREN („odlično izgleda"). ModernOffices2 ODOBREN. ModernOffice3 (folder `ModernOffice3`, mapa ModernOffices3.umap) izvezen, 0 grešaka; bio plav jer je UEFN sesija krenula noću → exporter od tada UVEK postavlja Time of Day 3 PM (Island Settings, preko helpera). Sledeći Modern Hospital.

Lista (29.9.2026, redom): Modern Offices ✔, Modern Offices 2. ✔, Modern Office 3 ✔, Modern Hospital ✔, Office Park ✔, Abandoned Office Park ✔ (29.9. 23:30), pa ControlRoom, ControlRoom 2, ControlRoom 3 (Dejan dodao: sveže sa Faba, zbog monitora i smoke efekata; stare UEFN\Test3/4/5 NE dirati).

30.9.2026 popodne, lista 2 (Playground and Park→Playground, Museum, Museum 2→Museum2, The Coffee Stop→TheCoffeeStop, SciFi Corridors→SciFiCorridors, SciFi Corridors 2→SciFiCorridors2): Dejan „radi do kraja bez slika, preskoci sta ne moze, pa ugasi kompjuter". Skripte u scratchpad: fab_search.sh, fab_add.sh, uefn_validate.sh, export_result.sh; new_ue_project.sh je gubio .uproject (popravljeno).

30.9.2026 oko 10:50, Dejan „svaku zgradu pogodi ovako bice odlicno": visina paketa se racuna od vrha NAJNIZEG ravnog mesha (floor panel), X/Y ostaje sredina najvece sobe (UEFNLevel.cpp, GroundTop). Pre toga je paket tonuo za visinu sprata (ModernOffice 9.4 m). PAZI: druga Claude sesija (chat „Unreal to Unity exporter") ume istovremeno da vozi UEFN — pre gasenja UEFN proveri, jednom sam joj ugasio sesiju.

30.9.2026 prepodne, Dejan „sve radi kako treba bravo": ControlRoom 1–3 i ModernHospital ponovo izvezeni i provereni. Naučeno: (1) prazan UE projekat iz šablona NEMA distance fields → Lumen ne radi, scena i ikone tamne; `enable_lumen.py` sada ide u new_ue_project.sh, svih 9 projekata ispravljeno. (2) uefn_export_behaviors_device: „Visible in Game" je `visibleInGame` na samom uređaju (NE VisibleInGameComponent); postavlja ga EXPORTER (helper PlaceSounds.py), ne ja ručno. (3) Mesh >30k trouglova → 20k. (4) Atlas četvrtine u UI grupi, Never Stream. (5) Ekrani: crn BaseColor, samo emissive. (6) uefn_check.sh dupli-klikne PRVU pločicu u Recent Projects = poslednji otvoren projekat, ne traženi → biraj pločicu po imenu.

Stanje 30.9.2026 noću: ControlRoom, ControlRoom2, ControlRoom3 izvezeni, 0 grešaka, sesije rade; 4K atlasi monitora dele se na 4 × 2K (pravilo, u H:\UnrealToUEFN\CLAUDE.md), monitori oštri. OTVORENO: para (Cascade steam) prenesena i uvećana na 500 cm, ali se u sesiji ne vidi. Fab uvoz ide klikovima (Add meni > Fab > ikona My Library > pretraga > „+"); pre new_uefn_project.sh proveri da UEFN raspored panela nije pomeren (Content Browser dole).

Dejan 29.9.2026 uveče: od Office Parka radim SAM bez čekanja potvrde (pregledam, ako je ok sledeći), u ControlRoom paketima pazi na monitore (oštrina + UV offset) i prenesi paru (Cascade→Niagara); posle ControlRoom 3 UGASI RAČUNAR (on spava).

8.10.2026, lista 3 (Podcast Studio, Podcast Studio 2., Urban Photo Studio, Parking Garage, Gas Station, Basketball Arena,
Red Studio, Green Studio). PodcastStudio ✔, PodcastStudio2 ✔ (folder PodcastStudio2, mapa L_PodcastStudio2; 0 gresaka, sesije rade). Novo: UEFN 42.30 pravi root plugin pod GUID imenom
(`d3152bc9-....uplugin`), pa je exporter poredio paket sa GUID-om i pravio dupli folder → ispravljeno (BuildDestinations
poredi sa imenom foldera projekta). Postupak ovog puta: UE projekat = kopija Config/.uproject iz Museum2 (nov ProjectID,
ProjectName) + junction UE_MCP_Bridge; Fab: Add > Fab > My Library ikona > pretraga (SendKeys) > predlog „In: My Library" > „+";
UEFN New Project: Blank, polje Project Name je na (1680,904) kad je Blank izabran; mapu u Maps prevuci misem (drag), Move Here, OK,
desni klik koren > Update Redirector References > Delete Unreferenced; File > Exit. Launch Session dugme + Docs\uefn_session.ps1.
Nastavak 8.10 (Dejan: „radi do kraja, pa ugasi kompjuter"): Urban Photo Studio → folder `PhotoStudio` ✔, Parking Garage → `Garage` ✔,
GasStation ✔, BasketballArena ✔, RedStudio ✔ (mapa L_RedStudio), GreenStudio ✔ (L_GreenStudio) — LISTA 3 GOTOVA 8.10. uveče, sve 0 grešaka, sesije u igri.
Lista 4 (12.10.2026): Urban Photo Studio već urađen (folder PhotoStudio = Urban, build UrbanPho…; drugi paket je
„One Moment Photo Studio", beli studio — NIJE rađen), Esportz Studio → `Esportz` ✔, Space Night Club → `SpaceNightClub` ✔
(mapa u `MAps/`), Research Center → `ResearchCenter` ✔. Exporter naučio: /Engine/EngineMeshes/ se KOPIRA (Sphere iz
pretvorenog Cascade efekta nije u UEFN), kopiji meša se gasi BodySetup bSimulatePhysics (Illegal property override).
Lista 5 (13.10.2026): Modern Office 4 → `ModernOffice4` ✔, SciFi Props → `ScifiProps` ✔, Scifi Generators → `SCIFIGenerators` ✔,
City Hall → `CityHall` ✔ — sve 0 grešaka, Verse čist, validacija, u igri. Dejan 13.10: „prošli su modeli preko 50k poligona" →
exporter sada smanjuje GEOMETRIJU LOD0 (BakeSimplifyLOD0), a PRE exporta ide `Docs\FabUcitavanje\audit_meshes.py` (spisak
>30k trouglova / >20k verteksa iz izvora); posle exporta svaki sa spiska mora biti `Mesh.Simplified` u Report.txt. Verse se
proverava u uefn_run.sh (VERSE OK). Generisani LOD-ovi 100/75/50 % (Dejan). Teksture >1M teksela ne-pow2 → ResizeToPowerOfTwo.
Šablon projekta: `Docs\FabUcitavanje\ProjectTemplate` (stari UnrealProjects se brišu). Pruge na bršljanu u ModernOffice4 su IZ ORIGINALA.
Lista 6 (16.10.2026): Background Buildings → `BackgroundBuildings` ✔ (postoje DVA Dexsoft paketa tog imena; uzet prvi, zgrade sa
prozorima; drugi ljubičasti NIJE rađen), Blacksmith Workshop → `BlacksmithWorkshop` ✔, Music Bar → `MusicBar` ✔, The Bar → `TheBar` ✔,
Modular Port → folder `Port` ✔, Living Room → `LivingRoom` ✔. Sve 0 grešaka, Verse čist, validacija, u igri.
NOVO PRAVILO (Dejan 16.10.): PRE exporta pravopis i ne-engleska imena se ispravljaju u IZVORU (list_names.py → rename_by_name.py →
fixup_redirectors → save, bez ručnog nagađanja; duple imene iz različitih foldera ne diram). Folder `mesh` → `Meshes` (Verse tip).
Exporter: /InterchangeAssets/ funkcije se kopiraju u paket (MF_PhongToMetalRoughness u Port-u). rename_by_name.py je jedino sto sme
da menja imena; MI_PlasticBlack (Material sa MI_ imenom) NIJE pravopisna greska, ne diraj.
Zamke automatike: skriptom aktiviran prozor ostaje iza Discorda → MinimizeAll pa ShowWindow(UEFN); UE posle starta ide preko
taskbar ikone (preview → prozor); log prošlog UEFN-a daje lažan „LOADED" (gledaj samo nove redove); uefn_session.ps1 sad
pokušava Make Private do 30 puta (BasketballArena: veliki spisak, prvih 6 klikova promašilo).
Exporter naučio: RuntimeVirtualTexture klasa je ZABRANJENA u UEFN (private ne pomaže) → RVT asseti se ne kopiraju, RVT/PathTracingQualitySwitch
čvorovi se vade iz kopija (NeutralizeRefusedNodes); UDIM tekstura → logička veličina, Stretch na pow2 + Max 2048 (cook je padao).
Sesija: „Game in Progress" tek kad krene faza igre (~10 min posle ulaska) — znak je `EndGamePhase_ClientMetrics` u klijent logu,
NE prvo „WaitingToStart to InProgress" (to je čekaonica). Moderacija (linkovi na teksturama CityProps) samo upozorava.
Skripte u scratchpadu ove sesije: pack.ps1 (koraci), uefn_new.sh (Blank+Maps+redirektori), uefn_run.sh (sesija+snimak).

**Why:** Dejan želi da exporter uči na pravim paketima sa Faba, jedan po jedan.
**How to apply:** Uputstvo `H:\UnrealToUEFN\Docs\EXPORTER_UPUTSTVO.md` + CLAUDE.md u tom folderu. Ako se folder paketa u Content razlikuje od imena sa liste, važi [[feedback-uefn-project-named-after-content-folder]] — pitati. Vidi [[feedback-uefn-new-project-blank-template]], [[reference-uefn-launch-and-gpu]].

# Učitavanje paketa sa Faba (koraci i skripte)


**Šta je ovo:** Dejan daje listu paketa (slika ili tekst, npr. „Podcast Studio, Gas Station…"). Za svaki paket:
nov prazan UE 5.8 projekat → otvoriš ga → Fab → My Library → paket → „+" (Add to Project) → sačekaš download →
zapišeš folder paketa u Content i glavnu mapu → zatvoriš editor. Dalje ide exporter (UEFN ili Unity) po svom
uputstvu. Proces je proveren na 8 paketa 8.10.2026 (lista 3, UEFN). Vidi [[project-uefn-fab-pack-pipeline]].

**Skripte (trajno):** `H:\UnrealToUEFN\Docs\FabUcitavanje\` — `pack.ps1` (koraci), `screen.ps1` (snimak ekrana +
klik), `wait.sh` (čekanje). Pokreću se iz tog foldera. Parametar `-Root` / env `ROOT=` = folder u kome se prave UE
projekti (podrazumevano `H:\UnrealToUEFN\UnrealProjects`; za Unity exporter pitaj Dejana gde, npr. `H:\UnrealToUnityExporter\...`).
- `screen.ps1` snima ceo desktop u `screen.png` na **POLA veličine** → koordinate sa slike ×2 za klik.
  `-ClickX/-ClickY` (puna rezolucija, 2560×1440), `-Double`, `-Out putanja`.
- Kucanje: `[System.Windows.Forms.SendKeys]::SendWait('tekst')`. NE zvati svoju funkciju `Type` (PowerShell alias za Get-Content).

**Koraci po paketu (ime projekta = ime sa liste bez razmaka, npr. GasStation):**
1. `pack.ps1 -Step newue -Name GasStation [-Root ...]` — pravi `<Root>\GasStation`: kopira `Config\*.ini` i `.uproject`
   iz `H:\UnrealToUEFN\Docs\FabUcitavanje\ProjectTemplate` (od 13.10.2026; stari projekti se brišu; tu je Lumen/distance-field podešavanje — prazan projekat iz šablona
   NEMA distance fields pa je scena tamna), nov ProjectID + ProjectName u DefaultGame.ini, junction
   `Plugins\UE_MCP_Bridge` → `H:\UnrealToUEFN\Plugin\UE_MCP_Bridge`, i pokreće editor.
2. `ROOT=... ./wait.sh ue GasStation` → READY (čeka „Total Editor Startup Time" u `Saved\Logs\<Ime>.log`).
3. **UE prozor posle starta ostaje IZA Discorda** (skripta ga ne može dovesti napred): klikni UE ikonu na taskbaru
   (≈1048,1055 pune rez.; nekad treba 2 klika dok ne izađe preview), pa klikni preview glavnog prozora „<Ime> - Unreal Editor"
   (≈940,960). Uvek prvo `pack.ps1 -Step shot` i pogledaj sliku pre klikova — jednom su klikovi otišli u Discord.
4. Fab: u novom projektu se otvori plutajući **Content Browser** sa dugmetom **Fab** (≈1316,267). (Alternativa: Add meni
   (300,74) → Fab (346,196) = `-Step fabsearch`.) Fab prozor je mali, u sredini.
5. `pack.ps1 -Step mylib -Text 'Gas Station'` — klik na ikonu My Library (1658,272), polje pretrage (1200,272), kuca tekst,
   klik na predlog „In: My Library" (956,317). Pogledaj `screen.png`: kartica paketa (Dexsoft Games).
6. „+" na kartici = Add to project: `pack.ps1 -Step click -X 1170 -Y 522` (prva kartica; ako ih ima više, nađi pravu na slici).
   Dole desno izađe „Downloading <paket>".
7. `ROOT=... ./wait.sh download GasStation` — čeka da broj fajlova u Content miruje 30 s, ispiše folder(e) paketa i Maps.
   **Folder paketa često NIJE ime sa liste** (Urban Photo Studio → `PhotoStudio`, Parking Garage → `Garage`); mapa je
   obično `<Folder>.umap` ili `L_<Folder>.umap`, pored nje `Overview.umap` (pregledna, ne exportuje se).
8. Zatvori editor: ue-mcp `project(set_project, <uproject>)` pa `editor(stop_editor)`. Reci Dejanu da zatvaraš editor.
   UE i UEFN nikad istovremeno.

**Zamke:**
- `wait.sh ue` hvata i log PRETHODNOG pokretanja ako postoji — za nov projekat nema problema.
- Grep na kraj exporta mora biti tačan („ExportToUEFN: exported"), ne samo „ExportToUEFN:" (hvata i upozorenja).
- Modalni prozor izveštaja exportera blokira ue-mcp: pre exporta `editor(set_dialog_policy, pattern, response=ok)`.
- `execute_command` za dug export uvek istekne (timeout) — rezultat se čita iz loga/Report.txt.

**Why:** Dejan hoće da drugi chat (Unity exporter) sam pravi projekte i skida pakete sa Faba isto kao ovde.
**How to apply:** kad Dejan kaže „prouči ucitavanjeSaFaba" — pročitaj ovaj fajl i skripte, pitaj samo za Root folder
ako nije jasno, pa radi paket po paket.
