# UEFN pravila — sme / ne sme / uslovno

Stanje: **UEFN 42.20** (engine 6.0.0-58011042, `++Fortnite+Release-42.20`, procitano iz
`Engine\Build\Build.version`). Dokumentacija procitana **25.9.2026**. Pre rada ponovo proveriti
linkove iz tacke „Izvori", jer Epic menja pravila.

Kad se dva izvora razlikuju, UVEK vazi STROZIJE. Kolona „CoffeeHouse" je izmerena na
`UnrealProjects\CoffeeHouseTest` 25.9.2026.

Oznake:
- **SME** = dozvoljeno;
- **NE SME** = zabranjeno ili blokira objavu;
- **USLOVNO** = dozvoljeno uz uslov;
- **NEPOZNATO** = nije dokumentovano i mora se testirati.

---

## 1. Prenos iz UE u UEFN

| Pravilo | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| Prenos UE → UEFN je zvanicno podrzan (Migrate u Content folder UEFN projekta) | SME | — | D1 |
| Izvor mora biti UE 5.1+. Iz novije verzije u stariju ne moze. | USLOVNO | 5.8 → 42.20: format paketa je ISTI (UE5 object version 1018 na obe strane, izmereno) | D1 + merenje |
| Sadrzaj UEFN projekta je plugin sa mount point-om `/<Projekat>/` | cinjenica | Izmereno: UEFN asseti su pod `/CoffieHouse/...` | D3 + merenje |
| `/Game/` u UEFN-u je **Fortnite-ov** sadrzaj (`/Game/Athena/...`) | cinjenica | UE asseti sa `/Game/CoffeeHouse/...` bi pokazivali u Fortnite prostor, pa se MORAJU preimenovati pod `/CoffieHouse/` | merenje |
| Kako Migrate prepisuje `/Game/...` u mount point | NEPOZNATO | Aktivna greska na velikim paketima: FORT-1151106 (sept. 2026), teksture gube reference | F4, F5 |
| Migrate ne proverava kompatibilnost. Nedozvoljeni tipovi ostaju kao „unsupported asset type" i blokiraju test. | USLOVNO | — | D1 |
| Kopiranje aktera iz UE u UEFN pravi nedozvoljene reference i „skrivene izmene svojstava" | NE SME | Level se gradi u UEFN-u, ne kopira se | D4 |
| Migriran `.umap` | NEPOZNATO / rizicno | Poznate greske: `NavigationSystemV1`, Level Blueprint, landscape proxy | C3, F1 |
| Sadrzaj iz Epic IP foldera | NE SME | — | D1 |

## 2. Tipovi asseta

| Tip | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| Static mesh, materijal, instanca materijala | SME | 64 / 4 mastera / 99 instanci | D2, D14 |
| Sopstvene funkcije materijala (u projektu) | SME | 6 | D14 |
| Engine/Fortnite funkcije materijala | USLOVNO: samo one vidljive u Function Call cvoru | proveriti koje masteri zovu | F1 |
| Teksture | USLOVNO (tacka 4) | 225 | D6 |
| Level Sequence (preko Cinematic Sequence device-a) | SME, ali trosi mnogo memorije | 6 (`shot1`–`shot6`) | D24, B-izv. |
| Svetla (Directional, Sky, Point, Spot, Rect) | USLOVNO (tacka 7) | + svetla iz 2 BP-a | D15 |
| Post Process Volume | SME | — | D19 |
| Foliage (ISM/HISM, Foliage mode) | SME | — | D25, D12 |
| Landscape | USLOVNO (tacka 8) | nema | D20 |
| Voda: UEFN ima svoje alate. Za UE Water plugin se ne zna. | NEPOZNATO | nema | D26 |
| DecalActor (dokumentovan je samo Decal device) | NEPOZNATO | — | D27 |
| Niagara | USLOVNO: nisu dostupni svi cvorovi | nema | B-izv. |
| Zvuk: WAV, AIF, FLAC, OGG (MP3 ne) | SME | nema | D2 |
| **Blueprint sa logikom** (BP scripting) | **NE SME** | — | D5 |
| Level Blueprint | NE SME | — | F1 |
| Prop Blueprint („Convert to Prop", samo podaci) | SME | — | D45 |
| C++ i sopstveni pluginovi | NE SME | — | C4 |
| Pecen svetlo (`_BuiltData`, lightmape) | NE SME: UEFN je dinamicki (Lumen) | 2× `_BuiltData`, NE prenosi se | D4 |
| USD, Alembic, Substrate | van obima (Dejan) | — | — |
| Sopstveni fontovi i video | NE SME | — | B-izv. |

## 3. Materijali

| Pravilo | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| Najvise 500 instrukcija po materijalu | USLOVNO | izmeriti 4 mastera | D14 |
| Custom (HLSL) cvor | NE SME | nema (izmereno) | F2, F3 |
| Runtime Virtual Texture | NE SME | — | F2 |
| Color Ramp cvor | NE SME (za sada) | proveriti | F2 |
| Menjanje skrivenih svojstava sa default vrednosti (od 41.00 greska, blokira objavu): `bVisibleInRealTimeSkyCaptures`, `bReceiveMobileCSMShadows`, `bCastDistanceFieldIndirectShadow`, `bSelfShadowOnly`, `bTreatAsBackgroundForOcclusion`, `CastRaytracedShadows` | NE SME | exporter mora da ih vrati na default | F2, 41.00 |
| Dozvoljena izlozena svojstva: `bDisallowNanite`, `bRenderInMainPass`, `bRenderInDepthPass`, `BoundsScale` | SME | — | 37.00 |
| Preporuka: instance materijala svuda gde moze | preporuka | vec tako | D42 |
| Parametri materijala (scalar, texture, vector) su dostupni iz Verse-a | SME | — | D35 |

## 4. Teksture

| Pravilo | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| **Cooked velicina najvise 2048** (validator: „reduce its size to 2,048 or less") | **NE SME preko** | **71 od 225 je 4096** | D6, C1 |
| Dejanovo pravilo: tekstura najvise 2K | vazi | isto | CLAUDE.md |
| Izvor (source) najvise 4096 | USLOVNO | 4096 je na granici | D6 |
| Stepen dvojke (obavezno preko 1024×1024, osim UI grupe) | USLOVNO | svih 225 prolazi | D6 |
| Mipmape obavezne. `NoMipmaps` i `Never Stream` padaju na validaciji. | NE SME bez | proveriti | D6, D8 |
| Kompresija Default (DXT1/5), Mip Gen „From Texture Group" | preporuka | — | D6 |
| UI grupa najvise 2048, ne mora stepen dvojke. Cubemap najvise 1024 po strani. | USLOVNO | — | D6 |
| Budzet za teksture bez streaming-a (vrednost se ne zna) | NEPOZNATO | — | D6 |
| Preporuka za mobilne: 512 | preporuka | — | D30 |

## 5. Meshevi

| Pravilo | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| Preko 30.000 verteksa na LOD0 dobija se upozorenje; preporuka je najvise 20.000 | USLOVNO | najveci ima 14.961 (`SM_Tree1`), nijedan preko 20k | D9, D1 |
| Mesh sa 500+ verteksa mora imati vise od 1 LOD-a | NE SME bez | **1 mesh ima samo 1 LOD** | D9, D10 |
| **Minimum LOD for Quality: Low = 2, Mid = 2** (validator) | obavezno | postaviti na svim meshevima | D9, 42.00 |
| Preporuka 3 LOD-a (50 % / 25 %), LOD for Collision = 2 | preporuka | vecina ima 4 LOD-a | D10 |
| Kolizija obavezna, najvise 10 UCX | obavezno | proveriti | D7 |
| Nanite postoji samo na jacim platformama (DX12 PC), uz Fallback | USLOVNO | 1 mesh ima Nanite | D13 |
| Lightmap UV nepotreban (trosi memoriju) | preporuka | — | D9 |
| Po mogucstvu 1 materijal po meshu | preporuka | 16 mesheva ima vise | D12 |
| Z osa na gore, jedinice cm, DirectX normale | obavezno | UE vec tako | D7, D42 |
| Najvise 2 GB memorije za cook jednog mesha | NE SME preko | daleko ispod | D9 |

## 6. Imena (Fab + Verse)

| Pravilo | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| Samo engleska slova, cifre i `_` | NE SME drugacije | **3 teksture sa crticom:** `T_Ground042_4K-PNG_*` | D41 |
| Putanja najvise 140 znakova, racunajuci gornji folder | NE SME preko | najduza 106 | D41 |
| Verse identifikator: pocinje slovom ili `_`, bez razmaka | USLOVNO: inace ga digest TIHO preskoci | proveriti sva imena | D35 |
| Asset ne sme da se zove isto kao folder, Verse kljucna rec (`set`, `block`...) ili Verse API | NE SME | proveriti | D35 |
| Bez nejasnih imena foldera („Assets", „NewFolder") | NE SME | ok | D41 |

## 7. Svetlo i post process

| Pravilo | Status | CoffeeHouse | Izvor |
|---|---|---|---|
| Svetlo je dinamicko (Lumen). Pecen svetlo ne radi. | cinjenica | enterijer je bio pecen, pa ce izgledati drugacije | D4, D15 |
| **Svetlo ostrva iskljucivo od Point, Spot i Rect svetala je CRNO na vecini platformi.** Osnova moraju biti Directional i Sky. | USLOVNO | enterijer sa lampama je rizik | D15 |
| Sopstveno svetlo: „Disable All Time of Day Managers" + Environment Light Rig (samo jedan) | obavezno | — | D16, D18 |
| Auto Exposure je potreban uz Lumen (Lumen Exposure Manager) | obavezno | — | D15, D16 |
| Svetla i PPV po nivou kvaliteta (Lighting Scalability Manager) | SME | — | D17 |
| Iskljuciti senke gde nisu potrebne | preporuka | — | D30 |

## 8. Landscape

| Pravilo | Status | Izvor |
|---|---|---|
| UEFN ima Landscape mode | SME | D20 |
| Najvise **2048×2048 verteksa** (ili isto toliko u drugom obliku, npr. 4096×1024) | NE SME preko | D20 |
| Uvoz heightmape iz fajla (Import From File) | SME | D20 |
| Format heightmape i uvoz weightmapa iz fajla | NEPOZNATO | — |
| Sopstveni landscape materijal (Layer Sample, Layer Switch, Layer Blend) | SME | D22 |
| Runtime Virtual Texture na landscape-u | NE SME | F2 |
| Prenos landscape aktera u migriranom nivou | NEPOZNATO, zvanicno nedokumentovano | D1, C3 |
| Memorija: custom landscape je skup, a streaming proxy nosi mnogo kolizije | USLOVNO | D24, D8 |

Put za exporter: mape visine i slojeva (kod vec postoji u Unity exporteru) → uvoz u UEFN
Landscape mode → materijal i slojevi.

## 9. Ogranicenja ostrva i objave

| Pravilo | Status | Izvor |
|---|---|---|
| Memorija: **100.000 jedinica** (od 42.20 se prikazuje kao 300 MB) u bilo kom delu nivoa | NE SME preko | D8, D31 |
| Meri se kroz Project → Launch Memory Calculation, iz cook podataka | alat | D8 |
| Streaming mora biti ukljucen za validaciju | obavezno | D8 |
| Velicina projekta: 256 MB (Fab referenced) / 400 MB / 2 GiB. Izvori se razlikuju. | USLOVNO: vazi 256 MB dok se ne izmeri | D3, D13, C7 |
| Validacija blokira i test sesiju i objavu | cinjenica | D4 |
| Validacija na svakom snimanju (od 40.00) | cinjenica | 40.00 |
| Frame rate iznad 30 FPS | pravilo | D43 |

CoffeeHouse izvor zauzima 1.6 GB Content-a. **Velicina je realan rizik** i meri se posle
smanjenja tekstura na 2K.

## 10. Verse i ponasanje (za sitne Blueprinte)

| Ponasanje | Put | Status | Izvor |
|---|---|---|---|
| Vrti se | Prop Mover device, bez koda | USLOVNO: **samo 1 aktivan u isto vreme**, mesh mora u „prop" | B-izv. |
| Vrti se | Scene Graph `keyframed_movement_component` + Verse komponenta | SME (Beta, moze da se objavi). Vrti se i u editoru. | D38 |
| Vrti se | Verse na `creative_prop` (Epic primer `rotating_prop`) | SME | D34 |
| Menja slike | Verse: parametar teksture u materijalu + `loop` / `Sleep` | SME | D35 |
| Menja slike | device koji prikazuje sopstvene slike | NE POSTOJI | B-izv. |
| Oba | samo materijal (vreme + rotacija verteksa / atlas) | NEPOZNATO: proveriti dozvoljene cvorove | — |
| Treperi svetlo | Customizable Light (Flicker) ili `light_component` | SME | B-izv., D40 |

## 11. UEFN MCP

- Zvanican i ugradjen u UEFN (od 42.00). Traze se **Python Editor Scripting** + **UEFN MCP
  Toolsets** u Project Settings. Port 8001 (tacka „MCP" u CLAUDE.md).
- Nezvanicne prijave: Python je na nekim nalozima zakljucan i tada ne postoji ni u Project
  Settings. Ako se tako desi, UEFN strana se ne automatizuje.
- Prostorne vrednosti: Python toolseti rade u XYZ, a UEFN u LUF. Pozicije se proveravaju.

---

## Otvorena pitanja (testirati pre koda)

1. Da li 5.8 paket, preimenovan pod `/CoffieHouse/`, prosto kopiran u UEFN Content, radi i
   prolazi validaciju. Ovo je prvi test (jedan mesh + materijal + teksture).
2. Da li UEFN MCP/Python radi na Dejanovom nalogu, jer je od toga zavisi gradnja nivoa u UEFN-u.
3. Koje engine funkcije materijala masteri zovu i da li su dozvoljene. Broj instrukcija mastera.
4. Da li Cinematic grupa tekstura izuzeta od 2048 (ne oslanjati se na to).
5. Stvarni limit velicine projekta.
6. Da li Movable Point/Spot/Rect svetla sama za sebe prolaze validaciju.

## Izvori

- D1 https://dev.epicgames.com/documentation/en-us/fortnite/migrating-assets-from-unreal-engine-to-unreal-editor-for-fortnite
- D2 https://dev.epicgames.com/documentation/en-us/fortnite/importing-assets-in-unreal-editor-for-fortnite
- D3 https://dev.epicgames.com/documentation/en-us/fortnite/import-from-fab-in-unreal-editor-for-fortnite
- D4 https://dev.epicgames.com/documentation/en-us/fortnite/validation-and-fixup-tool-in-unreal-editor-for-fortnite
- D5 https://dev.epicgames.com/documentation/en-us/fortnite/uefn-vs-ue-in-unreal-editor-for-fortnite
- D6 https://dev.epicgames.com/documentation/en-us/fortnite/textures-best-practices-in-fortnite
- D7 https://dev.epicgames.com/documentation/en-us/fortnite/fortniteready-assets-best-practices-in-fortnite
- D8 https://dev.epicgames.com/documentation/en-us/fortnite/memory-management-in-unreal-editor-for-fortnite
- D9 https://dev.epicgames.com/documentation/en-us/fortnite/simplify-static-meshes-in-fortnite
- D10 https://dev.epicgames.com/documentation/en-us/fortnite/level-of-detail-lod-best-practices-in-fortnite
- D12 https://dev.epicgames.com/documentation/en-us/fortnite/reducing-draw-calls-in-fortnite
- D13 https://dev.epicgames.com/documentation/en-us/fortnite/talisman-environment-template-in-unreal-editor-for-fortnite
- D14 https://dev.epicgames.com/documentation/en-us/fortnite/material-nodes-and-settings-in-unreal-editor-for-fortnite
- D15 https://dev.epicgames.com/documentation/en-us/fortnite/lighting-and-lumen-quick-start-guide-in-unreal-editor-for-fortnite
- D16 https://dev.epicgames.com/documentation/en-us/fortnite/using-the-lumen-exposure-manager-in-unreal-editor-for-fortnite
- D17 https://dev.epicgames.com/documentation/en-us/fortnite/lighting-scalability-manager-in-unreal-editor-for-fortnite
- D18 https://dev.epicgames.com/documentation/en-us/fortnite/environment-light-rig-device-in-unreal-editor-for-fortnite
- D19 https://dev.epicgames.com/documentation/en-us/fortnite/intro-to-postprocessing-in-unreal-editor-for-fortnite
- D20 https://dev.epicgames.com/documentation/en-us/fortnite/landscape-mode-in-unreal-editor-for-fortnite
- D22 https://dev.epicgames.com/documentation/en-us/fortnite/editing-landscape-material-in-unreal-editor-for-fortnite
- D24 https://dev.epicgames.com/documentation/en-us/fortnite/project-size-tool-in-unreal-editor-for-fortnite
- D25 https://dev.epicgames.com/documentation/en-us/fortnite/foliage-mode-in-unreal-editor-for-fortnite
- D26 https://dev.epicgames.com/documentation/en-us/fortnite/water-tools-in-unreal-editor-for-fortnite
- D27 https://dev.epicgames.com/documentation/en-us/fortnite/decal-device-in-unreal-editor-for-fortnite
- D30 https://dev.epicgames.com/documentation/en-us/fortnite/mobile-optimization-in-fortnite
- D31 https://dev.epicgames.com/documentation/en-us/fortnite/42-20-fortnite-ecosystem-updates-and-release-notes
- D34 https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/creative_prop
- D35 https://dev.epicgames.com/documentation/en-us/fortnite/exposing-assets-with-asset-reflection-to-verse-in-unreal-editor-for-fortnite
- D38 https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/versedotorg/scenegraph/keyframedmovement/keyframed_movement_component
- D40 https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/versedotorg/scenegraph/light_component
- D41 https://dev.epicgames.com/documentation/fab/upload-unreal-editor-for-fortnite-source-to-fab
- D42 https://dev.epicgames.com/documentation/fab/asset-file-format-and-structure-requirements-in-fab
- D43 https://legal.epicgames.com/fortnite/developer-rules
- D45 https://dev.epicgames.com/documentation/en-us/fortnite/converting-assets-into-props-in-unreal-editor-for-fortnite
- MCP https://dev.epicgames.com/documentation/fortnite/uefn-mcp
- F1 https://forums.unrealengine.com/t/handling-content-validation-in-24-00/787539 (Epic)
- F2 https://forums.unrealengine.com/t/2446835 (Epic: Kev.EG, Flak)
- F3 https://forums.unrealengine.com/t/custom-node-missing-in-uefn-material-editor/2349701 (Epic)
- F4 https://forums.unrealengine.com/t/2764421 (Epic, FORT-1151106)
- F5 https://forums.unrealengine.com/t/major-migrated-assets-from-ue5-lose-their-inter-asset-references/690338
- C1 https://forums.unrealengine.com/t/1621889 (moderator, poruka validatora)
- C3 https://forums.unrealengine.com/t/2346276 (zajednica, migriran nivo pada na NavigationSystemV1)
- C4 https://forums.unrealengine.com/t/1973996 (moderator, C++)
- C7 https://forums.unrealengine.com/t/2742383 (zajednica, 2 GiB)
- „B-izv." = izvestaji istrazivaca 25.9.2026 (Prop Mover, Customizable Light, Niagara, fontovi,
  video, Sequencer). Linkovi su u tim stranicama pod dev.epicgames.com/documentation/en-us/fortnite/.
