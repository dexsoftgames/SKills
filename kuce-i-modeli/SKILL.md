---
name: kuce-i-modeli
description: Dejanova odobrena pravila za izradu srednjovekovnih kuća, ambara, nameštaja i propsa (Blender generatori → UV → Substance Painter → Unreal). Koristi kad Dejan traži da se pravi, popravlja, razvija (UV), boji ili uvozi kuća, ambar, krov, stepenice, prozor, nameštaj, krevet, kutija, kola ili bilo koji drveni model, ili kad kaže „pravimo nove modele".
---

# Kuće i modeli — Dejanova pravila

Sva pravila su ODOBRENA od Dejana (datumi u referencama). Ne menjati vrednosti bez traženja.
Odgovaraj UVEK na srpskom.

## Pre SVAKOG modela (hook — prođi listu)

1. **LOGIKA:** kako bi ga stolar/seljak stvarno napravio? Šta na čemu leži, šta nosi težinu, šta mora biti ravno
   (pod, sedište, površina za dušek). Ništa nelogično.
2. **KOSO? → seci pod uglom** (PRAVILO BROJ 1). Kosnik/ukrštenica se nikad ne pravi kao pravougli box: oba kraja
   isečena ravno uz lice stuba i grede (`brace()`/`mitred()` – bisect_plane). Važi u SVAKOM generatoru.
3. **MENJA PRAVAC? → jedna kriva greda** (sweep po Bezier/C1 krivoj, 6–10 segmenata), nikad dve spojene pod uglom.
4. **MERI, ne odoka:** deo u osi nosača; svi uglovi kraja računski UNUTAR nosača (rezerva ≥5 mm); ništa ispod
   poda, ništa ne viri kroz ploču. Komentar sa merom u kodu.
5. **NIŠTA NE VISI:** svaki ležeći deo dodiruje oslonac na oba kraja; greda koja leži na nečemu ULAZI 5–6 cm
   (nikad samo dodir); uspravne ulaze u gornju i donju poprečnu. Okrugli spoj ide do OSE okrugle grede.
6. **Uvek blago krivo:** jitter 0.5–1.5 cm + nagib ±1–2°, rotacija ±1°, skala ±3%, luk dužih greda. Krivina SAMO u
   ravni zida, nikad ka zidu. Podne daske, gazišta i gornja strana podnih greda su RAVNI.
7. **Shading pre exporta:** smooth by angle 30° (+ Weighted Normal); obli delovi (oblice, kanap, valjci) glatki
   (atribut `rnd`), presečene kape oštre.
8. **Pre pokazivanja:** pogledaj model sa strane i izbliza (spojevi, odozdo), u Blenderu UVEK wire on shaded.
   Merenje nije dovoljno — otvori i POGLEDAJ.

## Tok rada

- Generator u Blenderu (Python, headless `blender -b --python ... -- spec.json`) → FBX → UV → Painter → Unreal.
- **Probaj na JEDNOM modelu/kući.** Masovni uvoz (sve kuće) SAMO kad Dejan kaže.
- Pre uvoza preko postojećeg asseta: uporedi broj trouglova i dimenzije sa ONIM ŠTO JE U UE, ne sa lokalnom kopijom.
- Model sa 3 stuba u redu → odmah i uska verzija `<ime>_2` sa 2 stuba (ista tekstura).
- Painter projekat posle setup-a pripada Dejanu: ne zatvaraj ga, ne otvaraj drugi preko njega, pitaj pre svakog
  kruga. Kad on nameštaj materijal — ne diraj ništa dok ne kaže „zapiši".
- Ne pokreći export ni uvoz sam bez dogovora. Nikad kopije/duplikate bez pitanja.

## Reference (čitaj po potrebi)

- [references/kuce.md](references/kuce.md) — kuće: grede i dubine, zidovi, prozori, vrata, škure, stepenice,
  podovi, krov, zabat, ambari, provera kuće, limit trouglova.
- [references/uv.md](references/uv.md) — UV: daska = jedno ostrvo, godovi po V, ≥75%, skriveno malo, pakovanje.
- [references/painter-unreal.md](references/painter-unreal.md) — Painter (GENERIC slojevi, drvo, propsi, bake) i
  standard uvoza u Unreal (M_MasterMain, VT, sRGB).
- [references/pipeline-alati.md](references/pipeline-alati.md) — putanje skripti na Dejanovim diskovima,
  Tripo/Maya pipeline, Painter most.

## Napomena o putanjama

Skripte (`E:\Tripo\...`, `E:\!Share\MedVillMegaFIN\...`, `H:\IzradaModela\...`) postoje samo na Dejanovom glavnom
računaru. Na drugom računaru važe PRAVILA iz ovog skilla; za skripte proveri da li folder postoji pre pozivanja.
