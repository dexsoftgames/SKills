# Kuće i ambari — odobrena pravila

Kod: `E:\!Share\MedVillMegaFIN\HouseBuilder\assemble_houses.py` (krov: `RoofLibrary\make_roof_frames.py`).
Biblioteke: PlankLibrary (daske/grede), WallLibrary (zidni moduli), FloorLibrary, RoofLibrary, HouseParts.

## Logički pregled SVAKE kuće pre slanja (Dejan 18.10.2026)

Sam uoči gluposti — Dejan ne sme da ih pokazuje. Uporedi sa pravim srednjovekovnim kućama.
- Sleme duž DUŽE strane, zabat na užoj; ulaz na dužoj strani, ispred ulaza kameni stepenik (pod 45 cm iznad zemlje).
- Terasa: svaka konzola/stub se oslanja na zid; ništa ne visi u vazduhu. Sprat dobija vrata napolje samo gde je terasa.
- U kući SAMO stepenice (bez kamina, dimnjaka, stola, kreveta, fenjera); propsi se rade posebno. Ognjište i dimnjak
  su posebni modeli koji se postavljaju u Unrealu, nikad u mesh-u.
- Nema rupa u zidu/zabatu/podu (holecheck zracima, rupu pokrij tankom daskom), nema dasaka koje vise.
- L-kuće: krov glavne kuće se odseca gde je krilo; krilo ulazi u krov do slemena.
- 2 sprata: prizemlje KAMEN, gore blato ili drvo.
- **Limit: 60.000 trouglova po kući** (Dejan 18.10.).
- Slike za Dejana: spolja 2–3, prizemlje 2–3, sprat 2–3 (`editor.set_viewport` + `capture_screenshot`; `capture_scene_png` daje crno).
- Svaki SPRAT od istih elemenata u krug — ne mešati dva različita drveta/zida na jednom spratu.

## Grede — dubina (ODOBRENO 19.10.2026, „sjajno")

- U grupi: kose najbliže zidu, pa vodoravne, pa uspravne; između grupa skok 4 cm. Nivoi se NIKAD ne preklapaju.
- Lice: tanke −2.5/−3.0/−3.5 cm; srednje vodoravne −7.5 / uspravne −8.5; debele vodoravne −12.5 / uspravne −13.5.
  Tanke nikad bliže od −2.5 (malter izbija do ~2.7 cm).
- Debeli stubovi ULAZE 4 cm u gornju i donju debelu gredu; gornje debele grede iznutra do +0.20, sill do +0.21
  (pokrivaju krajeve stubova). Debele poprečne pokrivaju preseke iznutra i spolja.
- Krivljenje greda SAMO uz zid (levo-desno, gore-dole), NIKAD ka zidu (cy/cz ≤ 0.2 → dubina se ispravlja).
- Sve noseće grede blago krive (loop ±1.6 cm bočno / 1.3 cm vertikalno + luk 0.5%); „pravo ko strela ružno do bola".
- Vodoravne grede zida se završavaju 5 cm UNUTAR uglova; ništa ne probija ugaoni stub ni krov.
- Ugaoni stubovi 30×30, donji se produžava 15 cm kroz procep između spratova (bez prekida).
- Na svakom spoju zidnih modula tanka vertikalna greda pokriva šav teksture.
- Nema izmišljenih dekorativnih greda (srednja vodoravna greda je obrisana). Zabat BEZ ukrasnih letvica (ni X, V, K).
- Ukrštene letve samo u PUNIM modulima blata, nikad preko prozora/vrata.
- Audit posle svake izmene: `AUDIT=1 blender ... assemble_houses.py -- spec.json` (otkriveni krajevi greda).

## Prozori (ODOBRENO 17.10. „e sad je perfektno")

- Stubovi 20×20 uz ivicu otvora (centar u0−0.05 / u1+0.05), nadvožnik/parapet samo preko modula sa prozorom/vratima
  (od spoja do spoja); parapet se prekida kod vrata. Bez letvica u prozoru.
- Škure: šarka na ivici stuba uz otvor x=±(w/2−0.04); otvorene nasumično 40–60°; 2 metalna valjka šarke (r 1.8, h 10 cm).
- Kameno prizemlje: mali procep 22×55 cm bez okvira, samo rešetke. Drveno/blatno: prozori sa okvirom i škurama.
- Na jednoj kući SAMO jedan tip prozora i jedna vrata; nikad dva prozora u susednim poljima ni dva u jednom modulu.
- Kameni luk (Door3/4, StoneLarge6) NIKAD na drveni zid.
- Kuće se grade BEZ krila vrata/prozora — samo okviri; krila su prefabi po `meta['doors'/'windows']`.

## Vrata

- Bilo koji modul i zid; ~1/3 kuća dva ulaza na različitim zidovima; 60% glavna vrata ka putu.
- Kod kuća na sprat nikad levi zid ni zadnji levi modul (stepenice).
- Otvorena ~130° napolje, 3 šarke. Nema posebne grede iznad vrata (nadvožnik drži otvor).

## Stepenice

- Gazište = daska 30 cm, uspon ~25 cm, gazišta PRAVA; bočne daske 20 cm, gazišta ulaze 2 cm u njih.
- Iza vrha stepenica bar 1–1.2 m poda pre zida. Visina glave ≥2 m (mereno uz kosu ravan, sada 2.23 m).
- Poslednja greda pred stepenicama je 10 cm tanja odozdo.
- Rukohvat UVEK položen (široka strana gore); stubići 90 cm iznad površine, 12×12.
- Rukohvat na stubu (KONAČNO 20.10.): u uglu se rukohvati seku PRAVO na licima stuba, gornja ivica rukohvata = vrh
  stuba, nema 45°. Prave stepenice: stubovi sa kosim vrhom, rukohvat preko. Rukohvati potpuno pravi.
- Ugaone (L): donji krak uz levi zid → odmorište u zadnjem levom ćošku → gornji krak uz zadnji zid.

## Podovi

- SVE podne daske u JEDNOM pravcu (preko greda, duž x kuće), gore i dole, za sve kuće.
- Podne daske RAVNE, bez rupa, preklop ~1.5%.
- Podne grede 10×20, gornja strana ravna, pomeraj samo bočno; završavaju se unutar nosača obima (bressummer 20×33).

## Krov

- Istorijski redosled: wall plate → tie beam → principals (+collar/king/crown) → sleme → podrožnice → obični rogovi
  → letve → drveni crepovi → greben → zabatne daske.
- Tie beam i wall plate 20×34, spušteni u zid (preklop); centralni debeo stub 20×20 u zabatu od slemena do dna zida
  (osim kad je na sredini prozor/vrata).
- Obični rogovi na ≤2.4 m, nikad tik uz okvir; letve 1.20 m. Rogovi vire 25 cm van pokrivke.
- Jedna ploča crepa po strani krova (mreža 1.2 m). Ništa ne probija krov; collar spušten i skraćen.
- Daske i krov LEŽE na poprečnim gredama (dno na izmerenom vrhu grede), jedna do druge, nikad jedna preko druge.
- Ivica krovne ploče: šav po gornjoj ivici, UV se otvara napolje.
- Okrugli prozor u zabatu ~40% kuća (boolean samo na delovima koje krug seče).

## Ambar (19.10. „mnogo bolje, bravo")

- Bez temelja; 4 okrugle krive grede u ćoškovima iznutra + okrugle poprečne gore/dole.
- Zid i zabat = stare krive daske (Wood049/059) jedna do druge (razmak 0.6–1.4 cm), krive van ravni, do zemlje;
  nigde dva sloja osim preklopa na krovu. Krov kao šindra.
- Vrata oba krila napolje 100–115°, samo valjci šarki. Prozor = rupa + okrugli okvir + krst.
- Zakrpe: 2–5 krivih dasaka preko zidova + 1–2 na krovu, leže na izmerenoj površini.

## Kontaktne senke (19.10.)

Trake uz grede (slot `Shadow` → M_ContactShadow: Modulate + Unlit + TwoSided, VertexColor.R), prate stvarnu krivu
gredu, 2 reda verteksa, korak 0.8 m. Blend/shading model menjati kroz ue-mcp, ne Python.
