# Painter i Unreal — odobrena pravila

## Painter — osnovno

- Pre svakog Painter koraka proveri da Painter radi i most odgovara: `python E:/Tripo/painter_do.py "OUT='ok'"`.
  Posle restarta Painter se ne pali sam.
- Painter projekat posle setup-a pripada Dejanu: ne zatvaraj, ne otvaraj drugi preko njega, PITAJ pre svakog kruga
  (`rebuild_set`, close, create). Pre zatvaranja snimi njegovu verziju.
- Kad Dejan nameštaj materijal: ne diraj ništa; na „zapiši" pročitaj parametre sa sloja i upiši u kod.
- Posle TaskStop-a pobij zaostale procese:
  `Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'painter_do|paint_groups|painter_export' } | Stop-Process`.
- Bake: više modela na jednoj teksturi → u FBX-u razmaknuti (širina + 2 m), inače AO hvata susede.

## GENERIC slojevi (`E:\Tripo\generic\README.md` — pročitaj prvo)

- Automatski na svaki model: GENERIC_GroundDirt, GENERIC_AO, GENERIC_EdgeWear (Metal Edge Wear generator).
- Po izboru (`NAMES=[...]`): Folds_*, Dirt_Light (slabiji), Dirt_Strong (jači).
- Komanda: `cd E:\Tripo` → `python painter_do.py -f generic\apply_generic.py`.
- Šavovi (`E:\Tripo\stitches\stitch_all.py`) uvek na VRHU steka, svaki sa Thread AO.
- Drvo: `generic\materials\apply_wood.py`, podrazumevano WoodWalnut (tiling 9, rotacija 84.19°), na dno steka.

## Propsi i nameštaj (ODOBRENO 20.10.)

- Nitne NIKAD geometrija — idu kao paint. Bez urezanih ornamenata, bez metalnih pločica.
- Spojevi do sredine nosača, noge/pojas 4 mm u sedište; `check()` pre Paintera.
- Grupe na 2K: 4 stolice / 2 stola / ~10 sitnih; svaka grupa svoj texture set.
- Završni izgled: WoodWalnut + EdgeWear tanji + GroundDirt + AO tamno braon + Dirt_Light; na vrh DirtFence pa 2.ao.
- Klupe/police: blago iskrivljene, sedišta i police ugnute nadole (sag), nikad procep.
- End Grain (TreeEnd005) samo na komadima koje Dejan traži.
- Čekaj Dejanov pregled u Painteru pre sledeće grupe.

## Unreal uvoz — standard (ODOBRENO 20.10. „isto ko u Painteru")

- Nameštaj: `/Game/MedievalVillage3/Furniture/<Chairs|Tables|Cabinets>`; SM_* u korenu, `Textures/T_<Set>_BaseColor|Normal|ORM`,
  `Materials/MI_<Set>`.
- MI je dete `/Game/Masters/M_MasterMain`; prekidači albedo/normal/occlusion/metallic/RoughnessTex = True,
  RoughnessMultiplier 1.4, EmissiveValue 0.
- Teksture SVE Virtual Texture; BaseColor sRGB, Normal i ORM non-sRGB. Normale iz FBX-a (Import Normals).
- Pack master M_MasterPainter1: parent MI mora biti MI_Balcony; Roughness 0.88–0.95 + Roughness Blend 0.75–0.8
  (inače mokre mrlje u senci).
- Uvoz preko postojećeg asseta istim imenom (čuva reference); pre toga uporedi geometriju sa UE originalom.
- Shading model/blend mode menjati kroz ue-mcp `material.set_*`, ne Python.
