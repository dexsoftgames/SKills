# UnrealToUEFN — uputstvo za rad

**Novi chat: prvo procitaj `Docs\EXPORTER_UPUTSTVO.md`** (kako exporter radi u UE i UEFN, redosled, pravila, otvoreno).

Projekat od 25.9.2026: exporter iz Unreala u UEFN (Unreal Editor for Fortnite).
**Nije vezan za igru Malo Seoce** (`H:\MaloSeoce2`), pa se ne mesa sa njom i tamo se ne dira nista.
Sestrinski projekat je Unity exporter u `H:\UnrealToUnityExporter`. Iz njega se uzimaju
znanje i kod, ali se tamo nista ne menja bez trazenja.

## GLAVNO PRAVILO — ime UEFN projekta = ime foldera u Content-u (Dejan, 29.9.2026)

**UEFN projekat se NIKAD ne zove kao Unreal projekat.** Zove se po imenu foldera paketa unutar
`Content` foldera Unreal projekta.
- Unreal `Test10` → `Content\AbandonedHospital` → UEFN projekat **`AbandonedHospital`** (ne `Test10`).
- Isto za svaki nov: Test1, Test2, ... — pre „New Project" u UEFN-u pogledati `Content\` i uzeti
  ime foldera paketa (ne `Developers`, `Collections`, `__ExternalActors__` i sl.).
- Vazi za svaki NOV UEFN projekat od 29.9.2026. Postojeci `UEFN\Test1..Test10` se prave ponovo kao
  novi projekti sa pravim imenom + ponovni izvoz (Dejan 29.9.: „nov projekat + export").

## GLAVNO PRAVILO — struktura UEFN projekta, glavna mapa UVEK u Maps (Dejan, 29.9.2026)

„glavna mapa ide u Maps folder, TO MORA UVEK!!" i „NE GLEDAJ UNREAL RULES, ovo je UEFN!!!!".
Vaze SAMO Fab UEFN pravila (UEFN Content Guidelines + upload-unreal-editor-for-fortnite-source-to-fab):
sortirano po tipu ili setu, jasna imena (ne „Assets"/„NewFolder"), samo engleska slova/cifre/`_`, bez
praznih foldera, putanja do 140 znakova (sa gornjim folderom), bez redirectora, bez `.py`, u zipu tacno
jedan projekat bez `Saved`/`Intermediate`. Unreal pravilo „Content ima jedan folder" NE vazi za UEFN.
**Dejan 29.9.2026 (KONACNO): ime projekta (npr. `AbandonedHospital`) ide SAMO JEDNOM, a unutra svi
podfolderi kao u paketu u Unreal projektu — sem ako UEFN ne zahteva nesto drugo (svoje foldere/stvari).**
Paket je sam projekat, nema dvostrukog foldera:
```
UEFN\<Projekat>\Content\
    Maps\<Projekat>.umap                     glavna mapa
    Meshes, Material, Texture, Sounds, ...   kao u Unreal paketu (sortirano po tipu)
```
U UEFN-u: `<Projekat>` > `Maps`, `Meshes`, ... (`<Projekat>` se vidi SAMO JEDNOM).
Exporter: `/Game/<Paket>/X` → `/<Projekat>/X` kad se paket zove kao projekat. Mapa `/<Projekat>/Maps/<Projekat>`.
Nov projekat: posle „New Project" u UEFN-u napraviti `Maps` u korenu, prevuci praznu mapu tamo
(Move Here), Update Redirector References → Delete Unreferenced Redirectors, pa tek onda izvoz.
UEFN-ovi sistemski folderi (`__ExternalActors__`, `__ExternalObjects__`, `Collections`, `Developers`) nisu nasi.

## Cilj (Dejanovim recima)

Plugin u Unrealu: ucita se nivo, pritisne se **Export To UEFN**, scena se analizira, postuju
se SVI zvanicni UEFN zahtevi, sta ne moze da predje otpada i upisuje se u izvestaj,
jednostavni Blueprinti (ventilator koji se vrti, displej koji menja slike...) opisu se u
JSON i pretvore u **Verse**, sve ode u folder, otvori se u UEFN i sve radi.

## Obim — sta Dejanovi paketi stvarno sadrze (25.9.2026)

- Static meshevi, teksture i materijali sa **1–3 master materijala** po paketu, plus instance.
- Sitni Blueprinti: nesto sto se **vrti**, **ekrani sa slikama** koje se smenjuju. Nista
  specijalno preko toga.
- Svetla, post process i nivo sa pecenim svetlom (`_BuiltData`).
- **NE koriste se USD i Alembic.** Za njih se ne pravi podrska i ne istrazuje se.
- **Nema lokalizacije.** Sve je na engleskom (imena, tekst, dokumentacija).
- **Stedi se za UEFN** (Dejan, 25.9.2026). Tekstura dobija granicu po NAJVECEM meshu koji je
  koristi, izmerenom u nivou (skala ukljucena): mesh < 20 cm → 512, mesh < 1 m → 1024,
  inace 2048. 16-bitni izvori prelaze na 8 bita (HDR na 16F). Sve se radi na kopiji.
- **Virtual teksture:** Dejanovi masteri ih koriste. Exporter NA KOPIJI iskljucuje VT na
  teksturama i prebacuje sampler-e (VirtualColor → Color, VirtualNormal → Normal,
  VirtualMasks → Masks...). Redosled je teksture → funkcije → materijali. Izvor ostaje VT.
- **Nanite se NE koristi.** Ako je negde slucajno ukljucen, exporter ga iskljucuje na kopiji
  (CoffeeHouse: 1 mesh).
- **Engine asseti** (`/Engine/...`, npr. `BasicShapes/Cylinder`) se KOPIRAJU i prenose kao
  obicni asseti, BEZ posebnog engine foldera (Dejan, 25.9.2026). Svaki ide u folder gde paket
  vec drzi najvise asseta iste vrste: mesh medju mesheve (`Meshes/Props`), materijal medju
  materijale, tekstura medju teksture, funkcija medju funkcije.
- **Substrate se NE koristi.** Materijali su klasicni. Provereno 25.9. na CoffeeHouse-u:
  nema Substrate ni Custom (HLSL) cvorova, iako config ima `r.Substrate=True`. Substrate
  se ne istrazuje i ne podrzava.
- Exporter se pravi za OVO, ne za opsti slucaj. Sve van toga ide u izvestaj.

## Raspored foldera (isti princip kao Unity exporter)

```
H:\UnrealToUEFN\
  Plugin\UnrealToUEFN\       JEDINI izvor koda exportera (uplugin + Source). Menja se samo ovde.
  PluginBuild\UnrealToUEFN\  izlaz RunUAT BuildPlugin (binarni paket). Rucno se ne menja.
  UnrealProjects\            izvorni Unreal projekti. Plugin se u njih NE stavlja.
  UEFN\                      UEFN projekti, npr. UEFN\CoffieHouse
```

**Plugin je na nivou ENGINE-a** (Dejan, 25.9.2026: „sta god otvorim samo pritisnem dugme").
- `J:\EpicGamesDownloadFiles\UE_5.8\Engine\Plugins\Marketplace\UnrealToUEFN` je JUNCTION na
  `H:\UnrealToUEFN\PluginBuild\UnrealToUEFN`.
- `EnabledByDefault: true`, pa je dugme **Export To UEFN** na toolbaru (`LevelEditor.LevelEditorToolBar.User`)
  u SVAKOM 5.8 projektu, ukljucujuci i Malo Seoce. Modul je tipa Editor, pa ne ulazi u
  spakovanu igru.
- Build ISKLJUCIVO kroz `H:\UnrealToUEFN\BuildPlugin.ps1`. Skripta pokrece RunUAT BuildPlugin,
  pa vraca `"EnabledByDefault": true` u spakovani .uplugin. BuildPlugin taj kljuc izbacuje, a
  engine plugin bez njega je iskljucen i dugme se ne pojavljuje. BuildId paketa mora biti
  isti kao u `Engine\Binaries\Win64\UnrealEditor.modules` (25.9: 55116800).
- Posle build-a se svaki 5.8 editor restartuje, jer je DLL zakljucan dok radi. Live Coding
  ovde nije osnovni put.
- Isto ime plugina NE sme da postoji i u projektu, jer bi projektni pregazio engine-ov.
- Junction se pouzdano prepoznaje po `du -sm` (junction daje 0) ili `Get-Item ... | LinkType`.
- **UE_MCP_Bridge** (plugin preko kog Claude upravlja editorom) je u DELJENOM folderu
  `H:\UnrealToUEFN\Plugin\UE_MCP_Bridge` (kopija v1.3.9 bez Intermediate, BuildId 55116800). Svaki
  projekat u `UnrealProjects\` ima `Plugins\UE_MCP_Bridge` kao JUNCTION ka njemu (26.9.2026).
  `EnabledByDefault: true`, pa nije potreban upis u .uproject.
- Projekti za testiranje: CoffeeHouseTest i Test2 do Test10. Test2–10 imaju prazan C++ modul
  `LandscapeExporter` (4 linije) koji ih cini C++ projektima. Ne brisati ga.
- Unity smece je obrisano 26.9.: `UnityExport\` folderi, `.uproject.bak` i veza na Unity exporter.
  Ne vracati ga.
- UEFN projekti su u `UEFN\`: CoffieHouse i Test2. Za svaki sledeci test Dejan pravi prazan UEFN
  projekat istog imena.

## Sta je vec utvrdjeno (25.9.2026)

- **UEFN:** `C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe`.
  Verzija: engine **6.0**, Fortnite Release **42.20**.
- **Izvorni Unreal:** 5.8, `J:\EpicGamesDownloadFiles\UE_5.8\` (Build.bat je u
  `Engine\Build\BatchFiles\`). Nije u Program Files ni u registru.
- **Razlika verzija 5.8 → 6.0** je prvo sto se proverava kod prenosa asseta.
- **UEFN projekat** `UEFN\CoffieHouse`: `CoffieHouse.uefnproject`, sadrzaj u `Content\`,
  Verse putanja `/dexsoft-games@fortnite.com/CoffieHouse`.
- Folder `.lore` u UEFN projektu je Epic-ovo verzionisanje: **ne dirati ga**.
- **Izvorni CoffeeHouse** (5.8) je kopiran u `UnrealProjects\CoffeeHouseTest` i to je prvi
  test. Nema Blueprinta, pa se exporter pocinje bez BP→Verse dela. Original u
  `H:\UnrealToUnityExporter\...` se ne dira.

## 0. Fab zahtevi za UEFN Source — OBAVEZNI, iznad svega ostalog

Dejan (25.9.2026): „OVOGA MORAS DA SE DRZIS". Izlaz exportera mora da prodje ove uslove,
jer bez toga paket ne moze na Fab. Svaka odluka u kodu se proverava prema ovoj listi.
- https://dev.epicgames.com/documentation/fab/upload-unreal-editor-for-fortnite-source-to-fab
- https://dev.epicgames.com/documentation/fab/asset-file-format-and-structure-requirements-in-fab (sekcija UEFN Content Guidelines)

Stanje procitano 25.9.2026. Pre rada ponovo otvoriti oba linka, jer Epic menja pravila.

**Projekat**
- Otvara se i radi u TRENUTNOJ live verziji UEFN.
- Kompajlira se cisto, ukljucujuci Verse. UEFN validacija prolazi bez gresaka i bez
  „consequential" upozorenja. Isto vazi i za entitete sa Verse komponentama i za NPC
  behavior skripte.
- Svi redirectori su pocisceni (Content Browser → Update Redirector References).
- Asseti su cookovani i projekat je u Fortnite tehnickim limitima (Memory Management,
  Fortnite-Ready Assets Best Practices).
- Sadrzaj mora biti sopstveni. Svaki fajl koji nije od Dejana ili Epica (fontovi, grafika,
  zvuk, kod, biblioteke) prijavljuje se kao third-party. **Svi paketi koji se ovde
  exportuju su Dejanovi (Dexsoft)**, pa exporter ne proverava vlasnistvo.

**Imena i folderi**
- Samo engleska slova, cifre i `_` u imenima foldera i fajlova.
- Putanja svakog asseta je do **140 znakova**, racunajuci i ime gornjeg foldera.
- Bez nekoriscenih foldera. Sortirano po tipu asseta ili po setu. Bez nejasnih imena
  („Assets", „NewFolder").

**Sadrzaj**
- Svi asseti su u ispravnoj medjusobnoj razmeri, sa Z osom na gore i istim smerom.
- Teksture: stranice su stepen dvojke gde je moguce. **Najvise 2048 po stranici.** To je
  Dejanovo pravilo (25.9.2026, „to znam sigurno") i strozije je od Fab-ovih 8192/4096.
  Kad se dva izvora razlikuju, UVEK vazi strozije ogranicenje.
- Meshevi: bez defekata materijala i vidljivih savova, sa ispravnom kolizijom i LOD-ovima.
  Modularni delovi imaju pivot za slaganje po gridu.
- Demo nivo je obavezan ako nesto postoji u viewportu. Bez z-fightinga i bez nerazumno
  preklopljenih poligona.
- Dokumentacija je na engleskom (web, .txt/.pdf ili video) ako je potrebno znanje za
  postavku.

**ZIP arhiva**
- Tacno JEDAN UEFN projekat (`.uefnproject`), kompletan: projekat, plugin fajl, sav sadrzaj.
- **Bez `.py` fajlova.**
- Bez foldera `Saved` i `Intermediate`.
- Bez sifre i enkripcije.
- Zip se testira u CISTOM UEFN projektu: otvara se, sve reference se razresavaju, demo
  nivo radi. Fab to NE proverava.

**Metapodaci listinga (Dejan unosi, exporter moze da pripremi)**
- Da li ima LOD-ova i koliko. Da li ima dodatnih kostiju ili izmena skeleta.
- Izjava o third-party softveru.

Posledica za exporter: izvestaj mora da navede svako krsenje ove liste po imenu asseta
(dugacka putanja, nedozvoljen znak, tekstura koja nije stepen dvojke ili je preko 8192,
third-party fajl...). Automatska ispravka ide samo kad je bezbedna. Sve ostalo ostaje
Dejanu na odluku.

## Stanje exportera (25.9.2026) — RADI

Prvi pun izvoz CoffeeHouse → UEFN\CoffieHouse: 0 gresaka, 481 MB (izvor 1617 MB). UEFN je
ucitao assete bez gresaka u formatu. Kod je u `Plugin\UnrealToUEFN\Source\UnrealToUEFN\Private\`:
- `UEFNExport.cpp`: tok (sakupi → kopiraj pod /<Mount>/ → ispravi → akteri → provera → deploy).
- `UEFNAssetRules.cpp`: pravila i ispravke asseta (teksture, meshevi, materijali, import data,
  soft reference, granica teksture po velicini mesha).
- `UEFNLevel.cpp`: rastavljanje nivoa i BP-ova i akteri kao EXTERNAL ACTORS UEFN mape.
- `UnrealToUEFNModule.cpp`: dugme, komanda `ExportToUEFN [dir] [-analyze] [-nodeploy] [-only=/Game/..]`
  i pamcenje UEFN projekta (sam ga nalazi u `UEFN\` pored `UnrealProjects\`).
- Izvestaj: `<Projekat>\Saved\UEFNExport\<Mount>\Report.txt` (+ .json, manifest.json,
  DeployedFiles.txt).

Pravila koja su se pokazala (ne menjati bez razloga):
- **UEFN se ZATVARA pre izvoza.** Inace drzi stare verzije u memoriji i pri snimanju ih vrati.
- Kopiranje ide po receptu Advanced Copy-ja (DuplicateSingleObject + ConsolidateObjects samo
  unutar kopija), jer Advanced Copy odbija engine sadrzaj.
- Mount point se registruje samo za vreme izvoza (ON_SCOPE_EXIT ga uvek skida).
- Deploy dira SAMO fajlove sa svoje liste (DeployedFiles.txt). Tudj fajl se nikad ne prepisuje.
- GUID aktera je deterministican (putanja izvora + labela), pa isti akter ide u isti fajl.
- Provera izlaza cita tabelu referenci preko asset registry-ja, a NE tekst fajla. Tekst daje
  lazne uzbune iz Interchange import zapisa.
- `FBodyInstance::CopyBodyInstancePropertiesFrom` je samo za sablone: assert i pad editora.
  Kolizija ide preko setter-a komponente.
- Posle `PostEditChange` na meshu build je asinhron: `FStaticMeshCompilingManager::FinishCompilation`
  pre citanja broja verteksa.
- **Okruzenje se NE prenosi** (Dejan, 25.9.2026): DirectionalLight, SkyLight, SkyAtmosphere,
  ExponentialHeightFog, VolumetricCloud, PostProcessVolume i engine sky dome (`/Engine/EngineSky/`),
  i kao akteri i kao komponente u BP-u. UEFN ima svoje (Time of Day, Environment Light Rig,
  Lumen Exposure Manager). Preneti su javili greske pri otvaranju u Fortnite-u. Lokalna svetla
  (spot, rect, point) OSTAJU. Dokumentacija kaze da su svetla i PPV „dozvoljeni", i zato je
  ovo promaklo: sve iz dokumentacije se proverava u UEFN-u pre nego sto se uzme kao sigurno.
- Min LOD Low/Medium = min(2, broj LOD-ova − 1). Mesh od 500+ verteksa dobija 3 LOD-a: **100 / 75 / 50 %** (Dejan 13.10.2026; na 25 % je brsljan u ModernOffice4 bio u prugama).
  **High se NE dira** (ostaje LOD0), iako Epic preporucuje High = 1: drvetu (SM_Tree1) auto LOD1
  nema grane, pa je u UEFN-u lisce visilo u vazduhu (Dejan, 25.9.2026).
- Max Draw Distance se puni samo gde je 0, po Epic-ovim „suggested pair values" (Cull Distance
  Volume stranica). Za svetla Epic nema broj; ista tabela se primenjuje na precnik dometa.
- UE MCP poziv za izvoz istice posle 30 s, ali izvoz nastavlja. Kraj se ceka u logu projekta:
  `LogExportToUEFN: Display: ExportToUEFN:`.
- **Posle restarta editor je na „Untitled" nivou** (EditorStartupMap u test projektima pokazuje na
  nepostojeci RacingTrack2). Izvoz praznog nivoa je 26.9.2026 obrisao 3397 nasih fajlova iz
  UEFN\Test2 (Deploy uklanja sve sto novi izvoz ne proizvede). Sada `Run` odbija /Temp/ nivo i nivo
  bez ijednog aktera za prenos, pre bilo kakvog kopiranja. Posle restarta: PRVO `level load` mape.
- **Pokvaren materijal ruši UEFN validaciju cele mape** („Failed to translate Material ...
  Validation failed"). M_GlassMain (CorporateBuilding, BilliardClub): Feature Level Switch bez
  Default i Component Mask bez ulaza. Kopija se popravlja samo ako se NE kompajlira:
  Default ← najvisi povezan nivo (SM6, SM5, ES3_1), Mask ← nula (`RepairBrokenMaterial`). Posle
  svih popravki `VerifyMaterialsCompile` kompajlira svaku kopiju, i sve sto i dalje pada je Error.
  U Test2 je Dejan rucno prebacio MI_GlassMain na M_Glass_Panels_NM i obrisao M_GlassMain.
- **Exporter NE dira koliziju** (Dejan, 26.9.2026: „za uefn samo se prenese"). Kolizija se pravi u
  IZVORU alatom Simple Collision Maker; preko 10 konveksnih oblika je samo Warning sa uputom na alat.
  Istorija: Auto Convex na kopiji je zatvorio vrata SM_Market4 (30→10 hullova), pa je sve automatsko
  menjanje kolizije u exporteru izbaceno.
- **Simple Collision Maker je od 30.9.2026 ZASEBAN engine plugin** `H:\SimpleCollisionMaker` (Dejan: nezavisan od exportera); iz ovog plugina je izbacen. Opis ispod i dalje vazi.
- **Simple Collision Maker** (ODOBRENO, Dejan 26.9.2026: „tvoja je bila sasvim dobra", „nema veze sto
  ima vise"): desni klik na StaticMesh u Content Browser-u (svaki 5.8 projekat) ili konzola
  `SimpleCollisionMaker /Game/..` (vise meshova odjednom, jedan Undo). Mesh → celije 10 cm → greedy
  boxovi → spajanje najjeftinijih parova dok spoj ne pokrije prostor igraca (vrata/prolaz ostaju
  otvoreni) → strane boxa naleze na povrsinu okrenutu ka toj strani (nikad ne otvara rupu) →
  stepenice kao kos box (debljina po stvarnoj masi) + ograde uz krak kao kos box istog nagiba (zid
  visi od 130 cm iznad nosnih ivica nije ograda). Menja IZVOR (Undo radi). SM_Market4 (snimljeno
  26.9.2026 12:33, ODOBRENO „ovo tvoje je sasvim dobro"): 25 boxova + 1 kos + 2 ograde.
  Dejanovo pravilo: bolje visak nego rupa — alat NIKAD sam ne brise boxove, visak brise Dejan.
  UEFN nema tvrdi limit (10 je Epic preporuka), boxovi su najjeftiniji za fiziku.
  NE dirati raspored/parametre bez zahteva. Prave krakove prepoznaje samo kad idu duz X ili Y osa
  mesha (kos krak pod uglom u samom meshu ide kao obicni boxovi); spiralne — vidi dole.
  Probano i odbaceno: popunjavanje prostora gde igrac ne ulazi, automatsko brisanje viska, i Auto
  Convex kao osnova za boxove (on popuni vrata; boxovi preko hullova mogu samo biti veci).
  Spajanje NEMA granicu od 10: ide dok spoj ne pokrije prostor igraca (zastakljen prozor = 1 box).
  Prostor igraca = ceo kvadratni otisak 60x60 cm slobodan (ne 5 tacaka — tanko staklo izmedju tacaka
  pravilo je lazna mesta za stajanje i prozor je ostao 8 boxova). Posle toga, 26.9.2026:
  SM_BlockGlassFramed 1, SM_BlockGlass2m 1, SM_FillColumns 1/1, SM_GlassWallBase 3, SM_BlockGlassElevator 4.
  Box koji drugi box pokriva celim presekom na jednom kraju se skracuje do njega (stubovi SM_Market4
  staju ispod grede nad vratima — Dejan).
  SPIRALNE STEPENICE (ODOBRENO 26.9.2026, „jako dobro"): niz gazista sa istim usponom i istim uglom
  okreta oko jednog centra (krug kroz tezista, najmanji kvadrati) → box po stepeniku okrenut po sredini
  gazista, dubok jedan uspon (NE kosa ploca: helikoid se ne da ravnom plocom, na spoju bi bilo 30-40 cm
  stepenika) + ograde spolja/unutra (vidi dole: po 3 stepenika). Vazduh iznad svakog stepenika i kose
  ploce do 170 cm je prostor igraca (MarkAboveStairs) — bez toga su se spajali blokovi preko celog
  stepenista (otisak 60x60 nema mesta na spirali jer se sledeca gazista dizu u njega).
  SM_ModernBuildingStairs: Dejanova ociscena verzija snimljena (30 stepenika + 60 ograda + 4 boxa).
  Box stepenika spirale lezi na PREDNJOJ ivici gazista (duza ivica obrisa okrenuta ka stepeniku
  ispod) i pruza se unazad preko klina — tako je Dejan rucno okrenuo donja 4 (alat sad 0.6-1.9° od
  njegovih). Pravougaonik moze da prati samo jednu ivicu klina; po simetrali su obe promasivale 4°.
  Box ide nanize kroz plocu dok je >=25% povrsine ispod puno (do najnize tacke kose spiralne ploce;
  sa 90% je ostajalo 20-40 cm ploce = 16 blokova koje je Dejan brisao). Oko boxa stepenika se cisti
  cela celija. Na oba kraja spirale, gde se podest nastavlja na visini sledeceg stepenika, dodaje se
  jos jedan isti box okrenut za jedan korak (Dejan: „stavi isti kao jedan dole sa rotacijom").
  ODOBRENO 26.9.2026 („ovo je perfektno sad, samo jedan visak"): SM_ModernBuildingStairs = 32 stepenika
  + 60 ograda + 18 obicnih. Ne dirati spiralni deo bez zahteva.
  Ograde spirale PO 3 STEPENIKA u jednom kosom boxu (Dejan: „napravis 3 komada pa ih spojis ... nama
  su glavni stepenici da se podudaraju"): prava tetiva od pocetka prvog do kraja treceg stepenika,
  nagib = uspon/tetiva, dubina = visina ograde + jedan uspon; pokriva tacno isecak prstena Near..Far.
  Unutrasnja ograda uz stub ima nagib ~58° (mali radijus) — to je ispravno. ODOBRENO 26.9.2026
  („ovo je perfektno", „bravo!!"): 75 = 32 stepenika + 20 ograda + 23 obicna.
  Dejanov fokus: alat mora dobro za STEPENICE i VRATA; obicne zidove radi Unreal box / Auto Convex. Dubinu koju stub/kapitel dodaje zidu Dejan ispravlja rucno;
  pravilo „strana ne sme da visi u vazduhu" je probano i izbaceno po njegovoj reci.
  ZAMKA: u Unreal render podacima normala trougla koja gleda NAPOLJE je (P2-P0)^(P1-P0). Obrnuti
  redosled je dao normale ka unutra: naleganje nije radilo (zid 40 cm dobio box 50 cm) a stepenice su
  nadjene po donjim stranama nosnih ivica. Ispravljeno 26.9.2026; SM_Market4 snimljen PRE ispravke.
- **Staklo M_Glass_Panels_NM ima ~1600-1700 instrukcija** i u CoffeeHouse-u i u Test2, a UEFN
  validacija ga prima u oba. 500 je Epic-ova preporuka, ne greska; Dejan: ne dirati.
- **Pregled posle izvoza** (ODOBRENO, Dejan 26.9.2026: „odlican izvestaj" — raspored ne menjati,
  samo dodavati na dno grupa): prozor sa OK posle SVAKOG izvoza, i sa dugmeta i iz konzole
  (`ShowSummary`). NE sme biti modalni (FMessageDialog): taj zaustavi editor dok se ne klikne OK,
  pa bi i MCP izvoz stao. Novi izvoz zatvara prozor prethodnog. Isti tekst je na vrhu Report.txt.
  Nove stavke se dodaju na dno svoje grupe u `Run` (`Line(...)`); upozorenja i greske se
  nabrajaju sami po pravilu.

Utvrdjeno 28.9.2026 (Test2 CorporateBuilding, Test3 ControlRoom3):
- **Svetla po ekspoziciji (ODOBRENO, Dejan 28.9.: „svetla sad izgledaju odlicno")**: EV izvora se cita
  iz unbound PPV-a sa rucnom ekspozicijom (formula iz CalculateManualAutoExposure: log2(f²·shutter·100/ISO)
  − bias; default bias = r.DefaultFeature.AutoExposure.Bias = 1.0). Svako lokalno svetlo × 2^(cilj − EV
  izvora), EV jedinice se sabiraju. Cilj = `UEFNExport.LightTargetEV` = **2** (8 je spalilo enterijer u belo,
  ×1 skoro nevidljivo). CorporateBuilding EV −4 → ×64, ControlRoom3 EV −1.7 → ×13.
- **SpawnActor mnozi transform sa rotacijom root-a iz CDO-a** (Actor.cpp PostSpawnInitialize).
  DecalActor i SpotLight imaju root na pitch −90 → svi dekali i spot svetla su bili okrenuti za 90°
  (dekali projektovali bocno, „ne vide se"). Resenje: `Params.TransformScaleMethod = OverrideRootScale`.
- **Postavljanje u UEFN mapu (ODOBRENO, Dejan 28.9.: „odlicno u centru je sad i na betonskom podu")**:
  cela scena se pomera tako da PlayerStart paketa padne u centar mape (tu
  su UEFN spawn padovi), a pod ispod njega (complex trace) na +2 cm iznad UEFN poda. Bez PlayerStart-a:
  sredina scene + najvisi „floor" mesh. ControlRoom3 je bio 279 m od centra.
- **UEFN default pod** (GridPlane akteri, klasa `/Game/Valkyrie/GridPlane`, prepoznaju se po tom tekstu u
  name tabeli jer UEFN 6.0 pakete 5.8 ne moze da ucita): brise se SAMO ako je sopstveni pod scene duzi od
  100 m (CorporateBuilding); mala scena (ControlRoom3, 37×20 m) stoji na njemu i pod se VRACA iz
  `Saved\UEFNExport\<Mount>\RemovedFromUEFN\`. Brisanje je PREMESTANJE u tu rezervu, nikad pravo brisanje.
- **UEFN renderuje sa `r.Substrate=1` i `r.DBuffer=0`** (videti u UEFN logu). Klasicni materijali se sami
  prevode; DBuffer dekali idu u GBuffer.
- **Izvor se nikad ne menja**: provera na kraju izvoza sada gleda i dirty MAPE (GetDirtyWorldPackages),
  ne samo content. CorporateBuilding dekali su u IZVORU pokvareni od kad je paket usao u Test2:
  MI_Decal_RoadLines_Solid daje ne-VT teksturu parametru koji master cita VirtualColor samplerom
  („expects texture to be Virtual" u svakoj sesiji) → izgled se menja od sesije do sesije (nevidljivi,
  bela mreza). Kopija za UEFN je ispravna (sampler Color). Izvor NE dirati bez Dejanove odluke.
- **Nova CorporateBuilding sa stora (5.6) ima 21 Text3D natpis** („3D Text" folder); bez Text3D plugina
  5.8 mapu ne vidi („unknown custom version"). U Test2.uproject je Text3D privremeno ukljucen; odluka o
  natpisima (brisanje ili pretvaranje u meseve za UEFN) jos nije doneta.
- **UEFN i UE 5.8 editor NE smeju biti otvoreni zajedno**: Test3 je dvaput pao na GPU (page fault u
  compute sejderu, 5. frejm) dok je UEFN radio; bez UEFN-a radi.
- **UEFN se otvara direktno**: `UnrealEditorFortnite-Win64-Shipping.exe "H:/UnrealToUEFN/UEFN/<Test>/<Test>.uefnproject"`
  — sam se prijavi (refresh token) i otvori projekat bez browsera. Redosled: izvoz → zatvori UE → otvori UEFN.
  (28.9. popodne: otvorio je samo Project Browser → „My Projects" → dvoklik na plocicu projekta.)
- **Engine sadrzaj koji UEFN odbija** („Disallowed reference", Test2 28.9.2026): `/Engine/EngineResources/WhiteSquareTexture`
  (M_Decals_Master). Iz EngineResources se kao referenca zadrzava SAMO `DefaultTexture` (prosao u Test3); sve ostalo
  iz tog foldera se kopira (`IsEngineCore`). EngineMaterials (DefaultDiffuse/DefaultMaterial/FlatNormal/WorldGridMaterial)
  prolaze kao reference.
- **Custom (HLSL) cvor UEFN odbija i u KOPIRANOJ engine funkciji.** `ObjectLocalBounds` (vuce ga MF_Wind biljaka u novoj
  CorporateBuilding) ima samo dva Custom cvora `GetPrimitiveData(Parameters).LocalObjectBoundsMin/Max.xyz`: na kopiji se
  menjaju ugradjenim cvorom Object Local Bounds (izlaz Min/Max) — `ReplaceKnownCustomNodes`, Fixed `Material.CustomNodeReplaced`.
  Svaki drugi Custom cvor ostaje Error. Test2 posle toga: 0 gresaka, validacija prosla, sesija radi (Game Mode).
- **PRAVILO OD 21.10.2026 (Dejan): spawn platforme idu na PlayerStart paketa.** Najveca soba samo kad nivo NEMA
  PlayerStart. BlacksmithWorkshop: PlayerStart je ispred kuce, a najveca soba (46 m2) je bila unutra. Visina i dalje iz
  izmerenog tla (FindGroundHeight). Pravilo ispod (28.9.) vazi samo za nivoe bez PlayerStart-a.
- **TEREN (Landscape) se prenosi od 21.10.2026**: `BuildTerrainForUEFNMap` cita visine i tezine slojeva iz izvora
  (FLandscapeEditDataInterface) i pravi ALandscape u UEFN mapi preko `ALandscape::Import` (external actor, teksture su
  pod actorom). Visibility sloj (ALandscapeProxy::VisibilityLayer) se NE uvozi (assert u engine-u, pad editora).
  Limit 2048x2048 verteksa (ili toliko u drugom obliku); preko toga sad Error `Level.TerrainTooBig` (secenje oko
  sadrzaja jos nije uradjeno). Blacksmith: 1765x2017, 215 komponenti, 8 slojeva, u UEFN-u radi.
  OTVORENO: posle izvoza sa terenom izvorna mapa je „dirty" (Error `Source.Modified`) — editor zatvarati bez snimanja.
- **Spawn = sredina NAJVECE SOBE** (Dejan 28.9.2026, izabrao umesto PlayerStart-a: ControlRoom2 PlayerStart je bio u
  vratima). `FindLargestRoomMiddle` (UEFNLevel.cpp): mreza tacaka poda (svaki sprat), zadrzava tacke sa krovom i zidom
  u >= 7 od 8 pravaca, spaja susedne bez prepreke u visini grudi; najveca soba, tacka najdalja od ivica. Bez sobe od
  4x4 m ostaje PlayerStart. ControlRoom2: soba 146 m2, igrac usred kontrolne sale.
- **VolumetricScatteringIntensity > 1 se spusta na 1** na kopiji: postavljen je za maglu paketa (ControlRoom2 0.01),
  a UEFN-ova je mnogo gusca. BP_Reflector x500 je u UEFN-u bio blistav plavi konus (Dejan: „mnogo jaka i plava").
- **Svetla iz Blueprint grafa (SetIntensity) → Verse** (Test4 BP_GreenLight, treperenje): svetlo koje graf menja
  pravi Verse kao Scene Graph svetlo (sphere/spot/rect_light_component) i ono NE ide u mapu. Verse uzima kandele:
  `CandelaPerUnit` = konverzija jedinica x isti faktor ekspozicije (x11 u ControlRoom2); po akteru polje `<Svetlo>_Cd`.
  Svetlo u EV jedinicama se ne prevodi (Blueprint ostaje statican, u izvestaju).
  Test4 ODOBREN (Dejan 28.9.2026 „bravooo"): spawn u sali, bez plavog snopa, monitori menjaju slike.
- **Event Tick → Add Relative/Local Rotation fiksnog ugla** (BP_Vent, RetroStudio2) = isto vrtenje kao RotatingMovement
  (`ReadTickTurning`, Verse `Spin`), ugao po frejmu x 60 fps (u Unrealu je i sam vezan za fps). Test6 „odlicno izgleda".
- Pad UE na Test5 (UEFNVerse.cpp): `FString::Find` sa pocetkom posle kraja stringa se vrati na poslednji znak; token
  koji je ceo string (`@M2@`) je citao van niza. Tokeni se traze samo kroz `NextToken`.
- **Stanje 28.9.2026 uvece: Test2..Test10 izvezeni i pusteni u UEFN sesiji, svi 0 gresaka, validacija prosla.**
  Snimci u `Docs\Screens\`. Test8 ostaje sa granicom 30k (Dejan), od Test9 vazi 20.000 verteksa.
- **Granica verteksa = 20.000** (Dejan 28.9.: strozije pravilo pobedjuje): LOD0 preko 20k se na kopiji smanjuje
  (Simplify, cilj 19.000). Kamere u Test8 (30k granica) provereno bez deformacije (`Docs\Screens\cam*_compare.png`).
- **Cascade → Niagara** (`UEFNEffects.cpp`, `bConvertCascadeEffects`): Epic-ov Cascade To Niagara Converter (Python,
  plugin je zavisnost exportera u .uplugin) radi na KOPIJI pod mountom `/UEFNConverted/`; /Niagara/ ostaje referenca,
  skripte konvertera se kopiraju. Sistem koji koristi konverterov `SpriteLockAxis` se IZOSTAVLJA (njegov enum ostaje
  referenca na plugin i UEFN odbija ostrvo; 5 pokusaja nije pomoglo). Test10: 4 od 5 sistema preneto, varnice rade u igri.
- **Zvuk (29.9.2026, AUTOMATSKI)**: UEFN NEMA AmbientSound ni AudioComponent — samo Audio Player device, a ta klasa
  postoji SAMO u UEFN-u (UE 5.8 ne moze da je upise u mapu; podesavanja su u ToyOptionsComponent kao parovi stringova).
  Verse `sound_component` je apstraktan/epic_internal, konkretne komponente UEFN pravi samo za MetaSound. Zato:
  1. Exporter kopira SoundWave/SoundCue i pise `Saved\UEFNExport\<Mount>\Sounds.json`. 3D zvuk nosi svoj min/falloff iz
     Unreala; 2D postaje 3D sa 3 m / 20 m (Dejan: „2d treba da pretvori u 3d i sve na ista mesta kao u unreal sceni").
  2. Posle deploy-a (`StartSoundPlacement`, UEFNEffects.cpp): brise fajlove uredjaja sa tagom `UEFNExportSound` iz
     `__ExternalActors__/<Map>` (prethodni izvoz; drugi izuzetak od „ne diraj UEFN fajlove", posle poda), upisuje
     `dataSets.experimental.toolsets.bEnableToolsetsForProject: true` u .uefnproject (tekstualno, proverava JSON) i pokrece
     `Resources\PlaceSounds.py` na Python-u iz engina (odvojen proces, prezivljava gasenje UE).
  3. Helper ceka UEFN MCP (port iz UEFN ini, 8001), da `get_current_level` = `/<Mount>/<Map>` (+20 s), sam ukljuci Python
     (`EnablePythonInUEFN`), pa za svaki zvuk: PlaceDevice, set_properties, labela `Sound_<ime>`, tag, save_actor.
     Log: `Saved\UEFNExport\<Mount>\SoundsPlaced.log`. Uvek se zavrsi: gotovo / noviji izvoz prepisao Sounds.json /
     12 h bez UEFN-a. Vec postavljene (isti label sa tagom) preskace.
  Test10 proveren 29.9.: izvoz → UEFN otvoren → 32/32 postavljeno samo, bez duplikata, sacuvano na disk.
  MCP nema brisanje aktera (zato brise exporter dok je UEFN zatvoren). Zvuk jos nije proveren sluhom.
- **30.9.2026 popodne (lista 2: Playground, Museum, Museum2, TheCoffeeStop, SciFiCorridors, SciFiCorridors2 — svi 0 gresaka, validacija prosla)**:
  `/Engine/EngineMaterials/Grid_N` nije u UEFN-u → kopira se u paket (IsEngineCore izuzetak); `/Engine/EditorMeshes/ColorCalibrator/`
  (M_ChromeBall na staklu) se kopira umesto da se referenca obrise; SoundCue `bOverrideAttenuation` UEFN odbija → na kopiji se
  iskljucuje (domet nosi Audio Player), iz Attenuation noda se seli samo AttenuationSettings asset. Paper2D flipbook se preskace.
  Visina: bez sobe → PlayerStart; soba se ponekad ne nadje kad meshevi jos nisu spremni (SciFiCorridors: prvi izvoz PlayerStart, drugi soba 47 m2).
- **uefn_export_behaviors_device — PRAVILO (Dejan 30.9.2026)**: kad se postavi u scenu, „Visible in Game“ je ISKLJUCEN:
  `visibleInGame = false` na samom uredjaju (checkbox u Details panelu; NE VisibleInGameComponent) (MCP set_properties + save_actor). Radi EXPORTER sam: helper `Resources/PlaceSounds.py` (`place_behaviors_device`) postavi uredjaj posle zvuka i iskljuci Visible in Game.
- **Imena PRE exporta (Dejan 16.10.2026: „ima dosta misspellinga ... srpski nazivi ... prevedi na engleski, updejtuj konekcije, pa export")**:
  prevodilac se NE ugradjuje u exporter; Claude u IZVORNOM UE projektu pregleda imena (`Docs\FabUcitavanje\list_names.py`), ispravi
  pravopis i prevede ne-engleska (srpski, francuski...: eolienne→WindTurbine, caisse→Crate, emmisive→Emissive, checkboard→Checkerboard),
  preimenuje preko ue-mcp `asset(bulk_rename)` (veze se azuriraju), `fixup_redirectors`, snimi, obrise prazne stare foldere, TEK ONDA export.
  Folder koji se zove kao Verse tip (`mesh`) → `Meshes` (`asset(move_folder)`), inace Verse.ReservedName. Pre exporta uvek i `audit_meshes.py`.
  Prozor „Redirector Update Report" blokira ue-mcp: `editor(set_dialog_policy, "Redirector Update Report", ok)`.
- **Poligoni — PRAVILO (Dejan 30.9.2026 „ne moze vise da prodje model koji ima vise od 30.000 poligona... skidas do 20.000“)**:
  svaki mesh ciji LOD0 ima vise od 30.000 trouglova smanjuje se na kopiji na 20.000, pored starog pravila za verteksе
  (>20.000 → 19.000). SM_ElectricBox6 (ControlRoom3) je imao 18.999 verteksa a >30k trouglova.
  **13.10.2026 (Dejan: „prosli modeli preko 50.000 poligona ... simplify iz modeling tools")**: smanjenje preko Reduction
  Settings NIJE bilo dovoljno — izvorna geometrija kopije je ostajala 50k+ (UEFN gradi mesh iz izvora). Sada `BakeSimplifyLOD0`
  smanjuje GEOMETRIJU LOD0 (IMeshReduction::ReduceMeshDescription, isti reducer kao Simplify/LOD-ovi), CommitMeshDescription,
  Reduction Settings LOD0 nazad na 100%. Broj se cita iz IZVORA (MeshDescription), ne iz render LOD0. Ako posle 3 prolaza
  ostane preko granice → ERROR `Mesh.Simplified` (ne Warning), i paket se ne pusta dalje.
- **Ekrani slajd-sou — (Dejan 30.9.2026 „odlicno izgledaju sad“)**: materijal koji cita atlas po celiji i vodi isti cvor u BaseColor
  i Emissive dobija crn BaseColor (`Material.ScreenEmissiveOnly`): UEFN svetla su x11 jaca pa su gornje monitore ispod lampi ispirala u belo.
- **Atlas monitora — PRAVILO (Dejan 29.9.2026 „ako ima tako velikih atlasa da se dele uvek. Jer se gubi ostrina“)**:
  atlas 4096 citan po indeksu (Floor u UV) deli se na 4 x 2048 (`SplitAtlasSamplers`, `SplitInstanceAtlases` u UEFNAssetRules.cpp),
  parametri `<Param>_Q0..Q3`; cetvrtine su u UI texture grupi, Never Stream, sa mipovima (World grupa je strimovana i
  Fortnite je smanjuje — ekrani „na ivici“, 30.9.2026); Verse (UEFNVerse.cpp) cita parametre sa STAGED kopije i replay-uje cetvrtine. Provereno u sesiji:
  ControlRoom, ControlRoom2 (dva atlasa: T_Atlas + T_AtlasNew preko MI_AtlasSlideShow2), ControlRoom3 — ostro, tacan offset.
- **Para (Cascade steam) — OTVORENO 30.9.2026**: konverter u 5.8 ne upise Sprite Size (ostane 10 cm) → exporter upisuje Cascade
  velicinu (500 cm) i kompajlira sistem pre snimanja. Ipak se u sesiji ne vidi; sledece: proveriti alpha krivu (ColorOverLife)
  i DepthFade/lit translucency u tamnoj sobi, uporediti sa originalom u PIE.
- **Staklo — ODOBRENO (Dejan 29.9.2026 „odlicno izgleda")**: teski glass shaderi (Thin Translucent + SceneColor,
  2440 instr.) su u UEFN-u nevidljivi. U izvornom Test10 napravljen `MasterMaterial/M_Glass_Simple` (19 cvorova,
  Translucent, Volumetric Directional = 485 instr., 3 teksture): albedo×Tint, alfa albeda = prljavstina/rupe
  (vise opacity + roughness), Frost 0.2, Refraction 1.05, normal preko Lerp „Normal Strength". Ista imena parametara
  kao M_Glass_Dirt, pa su MI_MedWallBGlassDirty, MI_BrokenGlassPartB, MI_Glass_Panels samo prevezani. Skripta:
  scratchpad make_glass.py/glass_apply.py. NE DIRATI vrednosti.
- **Panel staklo → jednostavno staklo, UVEK (Dejan 29.9.2026: „pa isto", „kad nadje panel master zameni sa simple pa
  export")**: `M_Glass_Panels_NM` je isti u svim paketima (110 cvorova, SceneColor, ~1625 instr.). Exporter ga prepoznaje
  po STRUKTURI (`IsPanelGlass`: Translucent + SceneColor + parametri Opacity/EdgeOpacity/TransmittanceColor) i na KOPIJI
  prepravi graf (`SimplifyPanelGlass`, UEFNAssetRules.cpp): 10 cvorova, Default Lit, **Surface ForwardShading** (pravi
  odsjaj), Color→BaseColor (crna), Specular, Roughness×0.5, Opacity = Saturate(Lerp(Opacity, EdgeOpacity, Fresnel)).
  Ime i parametri ostaju, pa instance (MI_Glass_Panels) ostaju vezane sa svojim vrednostima. Report: Fixed
  `Material.GlassSimplified`. Poredjeno slika uz sliku u ModernOffice: isto kao original; u UEFN sesiji staklo vidljivo.
  M_Glass_Dirt i ostala stakla imaju druge parametre i NE diraju se. ZAMKA: `UMaterialEditingLibrary::DeleteAllMaterialExpressions`
  brise iz niza koji obilazi i preskoci svaki drugi cvor — brisati iz KOPIJE liste.
- **Level Blueprint samo sa konzolnim komandama** (ModernOffices2: BeginPlay/Tick -> Execute Console Command
  "DisableAllScreenMessages", 29.9.2026): `IsConsoleCommandsOnly` (UEFNLevel.cpp) -> Info `Blueprint.LevelConsoleOnly`
  sa spiskom komandi. Bilo koji drugi povezan cvor, komanda iz pina ili funkcijski graf = i dalje Warning `Blueprint.LevelLogic`.
- ModernOffices2 (Fab „Modern Offices 2.", folder paketa `ModernOffices2`): 0 gresaka, sesija radi (29.9.2026).
- Scena u paketima je Lumen (ne peceno svetlo). Tamno kroz staklene pregrade = samo staklo (crno, Opacity 0.63 u ModernOffice).
- Nov izvorni projekat (od 29.9.2026): prazan UE 5.8 iz `Templates\TP_BlankBP` (Config bez TemplateDefs + .uproject
  EngineAssociation 5.8), `Plugins\UE_MCP_Bridge` junction, paket preko Fab → My Library → Add to Project. Config sablona se ne menja.
- Custom HLSL cvorovi `min(A,B)`/`max(A,B)` se menjaju ugradjenim Min/Max (Blend_Darken); prazan TextureSampleParameter
  u materijalu koji se ne kompajlira daje nulu iste sirine (M_Water_Test_01).
- Blueprint→Verse dodato: Set Timer by Function Name, Set Timer bez eventa (no-op), Add Local Rotation, SetVisibility,
  Intensity/bVisible svetla i mesha; handle metode su `UEFNGetMaterial()`/`UEFNGetComponent()` (folder `Material` u paketu
  se sudarao sa metodom `Material()`).
- Spawn: pretraga sobe gleda i visinu struka (70 cm) — sto/sank je ivica, pad ne ide pod sto (Test9).
- Prozor sa sazetkom izvoza blokira ue-mcp bridge: pre izvoza `editor(set_dialog_policy, "Export To UEFN", ok)`.
- Posle „New Project" u UEFN-u sacekati ~60 s pre gasenja, inace projekat ne udje u My Projects (Test5, otvoren
  preko Browse). „Make Assets Private" se pojavljuje na svakom Launch Session-u i trazi klik.

Otvoreno: optimizacija po Epic praksi (draw distance, senke, svetla) je u istrazivanju.
Instance se NE prave, jer kupac mora da pomera stvari pojedinacno (Dejan).

## MCP — rad u oba editora

`H:\UnrealToUEFN\.mcp.json` (Claude se pokrece iz `H:\UnrealToUEFN`):
- `ue-mcp` → izvorni UE 5.8 projekat (CoffeeHouseTest)
- `unreal-epic` → Epic-ov MCP u UE 5.8, `http://127.0.0.1:8000/mcp`
- `uefn` → **UEFN MCP**, `http://127.0.0.1:8001/mcp`. Zvanican i ugradjen u UEFN od
  20.8.2026 (https://dev.epicgames.com/documentation/fortnite/uefn-mcp). Toolseti: Verse
  (citanje, izmena, kompajl, greske), Verse Scene Graph, Creative Devices, Sessions (PIC test).

Gde UEFN to cuva (procitano iz UnrealEditorFortnite-Common DLL i UE 5.8 izvora, 25.9.2026):
- Port: `[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings] ServerPortNumber=8001`
  (+ `bAutoStartServer`), u `%LOCALAPPDATA%\UnrealEditorFortnite\Saved\Config\WindowsEditor\EditorPerProjectUserSettings.ini`.
  Klasa `UModelContextProtocolSettings`, config=EditorPerProjectUserSettings.
- Python Editor Scripting: klasa `ValkyrieExperimentalPythonSetting` (Experimental Access), pise u
  `[/Script/ValkyrieEditor.ValkyrieEditorConfig] EnablePythonLocallyPerProject` (mapa po ID-u projekta;
  ID je u .uefnproject `bindings.projectId`, isti format kao `TrustedProjectIds`).
- UEFN MCP Toolsets: klasa `ValkyrieExperimentalToolsetSetting`, polje `bEnableToolsetsForProject`,
  po projektu. Kad je ukljuceno, UEFN SAM pali MCP server pri otvaranju projekta
  („Started the ModelContextProtocol server on port %u for the UEFN MCP Toolsets setting").
  Tacno mesto upisa na disku jos NIJE procitano: posle prvog rucnog ukljucivanja pogledati diff
  config-a i .uefnproject-a, pa to upisivati automatski.
- Config se menja SAMO dok je UEFN zatvoren, jer ga UEFN inace prepise na izlazu.

Ukljucivanje u UEFN (rucno, jednom po projektu):
1. Project Settings: ukljuciti **Python Editor Scripting** i **UEFN MCP Toolsets** (Beta Access).
2. Editor Preferences → Server Port Number = **8001**. Na 8000 vec slusa UE 5.8 editor,
   pa bi se sudarili.
3. Restartovati UEFN. Server se pali i gasi samo restartom.

Zamke iz Epic dokumentacije:
- Prevod koordinata LUF → XYZ ume da pogresi prostornu matematiku, pa transformacije
  treba proveriti.
- Editor zastekce za vreme MCP poziva.

Fab: `.py` fajlovi NIKAD ne smeju ostati u UEFN projektu. Python skripte se drze van
`UEFN\<projekat>\`.

## 1. Prvo zvanicna dokumentacija — NE pretpostavljati

**URADJENO 25.9.2026 → `Docs\UEFN_PRAVILA.md`**, tabela „sme / ne sme / uslovno" sa izvorima
i merenjima na CoffeeHouse-u. Svaka odluka u kodu se proverava prema njoj. Spisak ispod je
ono sto je trebalo pokriti.


Izvor: dev.epicgames.com/documentation/en-us/uefn i Fortnite Island Creator Rules.
Pre ijedne linije koda napraviti tabelu „sme / ne sme / uslovno" sa linkovima:
- da li Migrate / uvoz .uasset iz UE 5.8 u UEFN (6.0) radi i pod kojim uslovom. Ako radi,
  vecina asseta prelazi DIREKTNO, bez rekonstrukcije kao za Unity.
- podrzani tipovi: static mesh, materijali (koji cvorovi i feature-i su zabranjeni),
  teksture, landscape, foliage, Niagara, sekvence, skeletal mesh, svetla, post process, voda
- zabranjeno: Blueprint, C++, sopstveni pluginovi; logika ide kroz Verse + Creative device-e
- memorijski budzet ostrva, limiti (akteri, svetla, velicina), pravila objave
- kako Verse pomera ili rotira prop i menja materijal ili teksturu u runtime-u (tacna API imena)
- kako se Verse fajl dodaje u projekat i kompajlira

## 2. Sta se uzima iz Unity exportera

Kod: `H:\UnrealToUnityExporter\Plugins\UnrealToUnityExporterWithLandscape\Source\UnrealToUnityExporterWithLandscape\Private\`

| fajl | sta daje ovde |
|---|---|
| `MaterialGraphAnalyzer` | citanje materijala po STRUKTURI grafa; ovde: nalazenje nepodrzanih cvorova pre prelaska |
| `SceneMeshExporter` | popis mesheva, LOD screen size-ovi, UCX kolizija, kes tekstura |
| `LandscapeUnityExporter` | obilazak scene i pisanje manifest.json; foliage kolizija po FOLIAGE TIPU, ne po meshu |
| `LightExporter`, `WaterExporter`, `DecalExporter` | svetla, voda (prepoznaje se po shading modelu), dekali |
| `SplineMeshBaker`, `FoliageAssetExporter` | pecenje splineova u geometriju, foliage asseti |

Kod se KOPIRA ili preradjuje u `Plugin\`; Unity exporter ostaje netaknut.

## 3. Nacela koja su se pokazala

- Prepoznavanje po strukturi, nikad po imenu asseta, jer mora da radi na svakom paketu bez
  podesavanja po paketu.
- Nista se tiho ne aproksimira: sve sto ne prelazi ide u izvestaj PO IMENU i sa razlogom.
- Svaka faza izolovana, pa greska u jednoj ne obara ostale.
- manifest.json je jedini ugovor izmedju strane koja cita i strane koja gradi.
- Merilo uspeha su slike istih mesta u Unrealu i u UEFN, ne broj objekata u manifestu.

## 4. Blueprint → Verse (predlog, potvrditi sa Dejanom)

Ne prevoditi graf cvor po cvor. Analizator obilazi BP graf (UEdGraph) i prepoznaje mali
skup PONASANJA po obrascu:
- stalna rotacija (Tick ili Timeline + AddLocalRotation)
- klackanje i lebdenje
- smena slika (niz tekstura + Delay/timer, ili parametar materijala)
- treperenje svetla
- ukljuci/iskljuci na preklapanje

Svako ponasanje ide u JSON opis (tip, osa, brzina, lista tekstura, period...), a iz njega
nastaju Verse sablon i Creative device u sceni. Graf koji ne odgovara nijednom obrascu ide
u izvestaj, bez nagadjanja.

**Odluka 28.9.2026 (Dejan): SVE sto Blueprint radi ide u Verse**, radi paralelno kao u BP-u.
Ponasanje se trazi i u GRAFU i u KOMPONENTAMA (RotatingMovement vrti i bez ijednog cvora).
ControlRoom3 ima 4 vrste: dugmad (tajmer + nasumicni EmissiveValue i Color na DMI), ekrani
(atlas Cols×Rows, sledeci slajd posle nasumicne pauze, pretapanje, redom ili nasumicno),
propeleri (RotatingMovement, Yaw = RandomFloatInRange na BeginPlay), reflektori (Delay petlja
ColorsSwitchON/OFF). Prvi dokaz: propeleri.

Sta Verse u UEFN 42.20 ume (procitano iz digest fajlova u
`%LOCALAPPDATA%\UnrealEditorFortnite\Saved\VerseProject\<Projekat>\Digests\`):
- svaki nas mesh postaje `SM_X := class(mesh_component)` sa `var <slot>:material` po slotu;
  svaki materijal `MI_X := class(material)` sa `var Param:float/color/texture` (parametar sa
  razmakom u imenu se preskace);
- Scene Graph: `entity{}` + `AddComponents` + `GetSimulationEntity[].AddEntities`,
  `transform_component`, `keyframed_movement_component` (SetKeyframes + loop mode),
  `light_component` (point/spot/rect: Enable/Disable, ColorFilter);
- Verse.org/SpatialMath je Left/Up/Forward — prevod iz XYZ (FromTransform/FromVector3) proveriti.
Exporter ne moze da postavi Verse device iz 5.8 (klasa postoji samo u UEFN-u): ili jedan rucni
korak, ili UEFN MCP (Creative Devices toolset) kad se ukljuci za projekat.

## 5. Pravila rada sa Dejanom

- Git: samo citanje. Bez commit, push i reset; on cuva dnevne backup kopije.
- Export i uvoz se NE pokrecu bez izricitog odobrenja (export brise izlazni folder).
- Samo jedan Unreal editor u isto vreme. Reci kad zatvaras editor; za build ga zatvaras
  sam (prvo save).
- Pre svake izmene proveriti sta ona moze da pokvari (pozivaoci, putanje izlaza), i posle
  izmene reci sta je jos dirnuto i zasto je bezbedno.
- Menjaj samo ono sto je trazeno. Kad kaze „odlicno", ne eksperimentisi dalje na istom.
- Pise na srpskom, kratko. Odgovarati na srpskom.

## 6. Prvi koraci u novom chatu

1. Ponovo otvoriti oba Fab linka iz tacke 0. Zatim procitati zvanicnu UEFN
   dokumentaciju i napraviti tabelu iz tacke 1, uskladjenu sa tackom 0.
2. Proveriti da li UE 5.8 asseti ulaze u UEFN 6.0 (Migrate). Od toga zavisi ceo pristup.
3. Tek onda predlog arhitekture plugina u `Plugin\`, pa potvrda od Dejana, pa kod.
