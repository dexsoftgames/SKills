# UV — odobrena pravila (Dejan 22–23.10.2026)

## Hook pre SVAKE operacije

1. Svaka daska, letva, oblica i PLOČA = JEDNO ostrvo, ručno otvoreno, nikad automatski.
   - Daska/kocka/kvader = krst: vidljivo lice u sredini, bokovi uz ivice, zadnja strana uz jedan bok.
   - Ploča = mreža kutije (`panel_net` u `E:/Tripo/uv_unfold.py`); ploča sa zaobljenim obrisom: lice i naličje celi,
     debljina okolo jedna traka.
   - Oblica: pravougaonik obim × dužina, jedan uzdužni šav, 2 kruga zakačena jednom ivicom.
   - Tanjir/činija: krug gore + krug dole + jedna traka. Vaza/krigla: telo pravougaonik, usna prsten, krug dole.
   - Kutija od 4 zida u jednom mesh-u = 4 daske.
2. NIŠTA ne štrči: nema lepeza, kosih ni razvučenih traka. Kraj se lepi uz svoju dasku pod pravim uglom.
   Odvojena traka sme samo ako je USPRAVNA (osna).
3. **Godovi uzduž**: duža osa svakog drvenog dela po **V** (WoodWalnut u Painteru ima godove po V).
   Ne postoji daska sa poprečnim godovima.
4. Preklop = 0 (Blender Select Overlap, `bl_overlap.py`). Bez ogledala: (dU × dV)·normala > 0.
5. NACRTAJ UV mapu samo drveta i POGLEDAJ je pre Paintera — brojke nisu dovoljne.
6. Seci samo dugačku dasku, i samo kad to diže popunjenost. Nikad ne seci ploču ni oblicu.

## Popunjenost

- Granica **75%** (Dejan: „možeš da ideš do 75"). Izuzetak: duge daske koje ne smeju da se okreću/seku (L6 krevet 67%).
- NIKAD Smart UV Project za finalni UV.
- Skriveni zidovi se brišu pre UV-a (dno na zemlji, donja strana dna/poklopca).
- Potpuno nevidljive površine (dno dušeka/jastuka) se odseku i drastično smanje; čim se deo površine vidi → maksimum.
  Redosled: prvo vidljivo raširi na maksimum, pa nevidljivo uglavi u prazna mesta (`uv_unfold.fill_hidden`).
  Packer bez izjednačavanja gustine (`UVPACK_RESCALE=0`).
- Ćebe = jedan pravougaonik.
- Pakovanje: `E:/Tripo/uvpack80.py` → `pack80([obj], res=2048, pad=3.0)` (Packer-IO, Keep Borders, bez sopstvenog
  sečenja). Razmak 3 px na 2K.
- Kanap/duge cevi: UV u komadima ~40 cm.

## Profi trik — okrenuta ostrva (ODOBRENO na Beds11)

Ostrva drveta smeju 90° radi popunjenosti. U Painteru duplikat drveta `<IME>_Poprecno` sa rotacijom +90° u
materijalu (WoodWalnut 84.19 → 174.19), maska = samo okrenuta ostrva, sloj IZNAD običnog drveta.

## Tripo mašine (Blender, 12.10.2026 „izgleda dobro")

`logic_live.py` (šavovi na tvrdim ivicama >50°, cev jedan uzdužni šav na skrivenoj strani, spajanje ostrva bez
razvlačenja) → `straighten_live.py` (Follow Active Quads) → pakovanje po materijalu. Pre shading-a obriši
custom split normals pa smooth by angle 30°.

## Ne koristiti

RizomUV (već loše), UnWrap3 za drvo (okreće ostrva), QuadRemesher (samo čišćenje non-manifold).
