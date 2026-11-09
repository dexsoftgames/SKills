---
name: tripo-cleanup
description: Dijagnoza i popravka gresaka na Tripo / AI generisanim modelima u Blenderu (rupe, non-manifold, duplikati, obrnute normale, losa topologija) uz QA verdikt sa screenshotovima. Koristi kad Dejan kaze "ispravi Tripo model", "ocisti model u Blenderu", "popravi greske na modelu".
license: MIT
metadata:
  domain: blender
  related-skills: blender-director, retopology, uv-workflow, asset-optimization, qa-review
---

# Tripo cleanup (Blender, preko MCP-a)

Skripta: `C:/Users/dejan/.claude/skills/tripo-cleanup/tripo_cleanup.py`
Ucitaj u Blenderu preko `execute_blender_code`:
`exec(open(r"C:/Users/dejan/.claude/skills/tripo-cleanup/tripo_cleanup.py").read())`
pa `diagnose(obj)` (samo cita) i `repair(obj, ...)` (menja mesh).
Headless provera bez MCP-a: `blender -b --python tripo_cleanup.py -- model.fbx [out.fbx]`
(Blender 5.0 je u `C:\Program Files\Blender Foundation\Blender 5.0`).

## Postupak (ne preskakati redosled)

1. **Pregled**: `get_scene_info`, pa `look` iz 3/4, spreda, sa strane i u wireframe-u. Zapisi sta se vidi golim okom
   (rupe u povrsini, cepanje, proboji, izduzeni trouglovi, zgnjeceni delovi).
2. **Dijagnoza**: `diagnose(obj)` za svaki mesh. Gledaj `boundary_edges`, `nonmanifold_edges`, `zero_area_faces`,
   `duplicate_verts`, `islands`, `ngons`, `negative_scale`. Skala: primeni (Ctrl+A) pre bilo cega ako nije 1.
3. **Odluka po objektu** (vidi tabelu). Ne popravljaj naslepo: svaki broj mora da se uskladi sa onim sto `look` pokazuje.
4. **Popravka**: `repair(obj)` pa opet `diagnose`. Uporedi pre/posle i `look` iz istih uglova.
5. **Topologija** samo ako treba (vidi `retopology` skill): Voxel Remesh / Quadriflow za haos, Decimate (Planar) za prevelik broj poligona.
6. **UV/materijal**: nove face koje je napravila popravka nemaju UV. Proveri u UV editoru; ako ima vise od par, ponovo unwrap (`uv-workflow`).
7. **QA verdikt** po `qa-review`: SHIP / SHIP WITH NOTES / NO-SHIP sa screenshotovima pre/posle.

## Sta znace brojevi

| Simptom | Znacenje | Akcija |
|---|---|---|
| `duplicate_verts` > 0 | Pocepani sesovi | `repair` radi merge by distance (1e-4; za male modele smanji) |
| `zero_area_faces` | Degenerisani trouglovi | `repair` ih brise |
| `boundary_edges` mnogo, a islands vise | Delovi su namerno odvojeni ili tanke povrsine | **Ne zatvaraj slepo.** Pogledaj `look`; zatvori samo ako je rupa greska |
| `nonmanifold_edges` > 0 | Ivica deli 3+ lica (T-spoj, unutrasnje face) | Rucno: selektuj (Select Non Manifold), obrisi unutrasnje face ili razdvoji delove. `repair` ovo NE resava |
| Normale kao "zebra" u Face Orientation | Obrnute normale | `repair` radi recalc napolje (pogresno na otvorenim tankim ljuskama; proveri) |
| Jako neravnomerni trouglovi / zumbasta povrsina | Losa AI topologija | Remesh, ne popravka |

## Provereno uzivo na `Machines/1 water_pump.fbx` (Blender 5.0, MCP)

- 84 non-manifold ivice = vertikalna rebra hlađenja na motoru (tanka rebra bez debljine). Vizuelno bezopasno, ne diraj.
- 3 189 otvorenih ivica = 312 petlji, 180 sa <=8 ivica, najveca 74. Sve na spojevima delova (prirubnice, nogari, poklopci).
  To su sesovi izmedju zasebnih skoljki, ne rupe. Zato `repair` po defaultu ne zatvara rupe (`hole_sides=0`).
- Kako pogledati: edit mode, `bpy.ops.mesh.select_non_manifold(...)` pa `view3d.view_selected()` i `look`.
- Model je vizuelno cist. Prave greske trazi ocima (shading, proboji, deformacije), ne samo iz brojeva.

## Ogranicenja starog testa (hole_sides=64)

- Pre: 21 712 face, 3 189 otvorenih ivica, 84 non-manifold, 2 degenerisana, 240 ostrva.
- `repair` je zatvorio otvorene ivice sa 3 195 na 729, obrisao 2 degenerisana, ali **non-manifold ostaje 84**,
  dodao 246 n-gonova bez UV-a, i 729 ivica je ostalo otvoreno (rupe vece od limita ili nepravilne).
- Zakljucak: automatika cisti lak deo; non-manifold, velike rupe i n-gonove treba gledati ocima i resavati po delu.
- Ako se model deli na delove za Mayu/Painter (pipeline), otvorene ivice izmedju delova su normalne. Ne spajaj delove.
- Dimenzije se ne smeju promeniti: posle popravke uporedi `dims`.

## Pravila

- Radi na kopiji (duplikat objekta ili sacuvaj .blend pre), nikad jedini primerak.
- Ne menjaj ime, pivot ni skalu objekta bez razloga; ne brisi materijale.
- Kad nesto nije jasno sa slike, reci Dejanu umesto da pogadjas.

## Opsta pravila

Pre rada procitaj `../references/verification-rules.md` (meri brojevima, API pre koda, quad topologija i budzet, petlja modeluj-izmeri-pogledaj).

## Test na `Props/1 scifi_cargo_a.fbx` (sanduci/burad, 25 164 face-a) - sta radi, a sta ne

- Sweep je prijavio 6 405 "obrnutih" face-ova (25%). **To je bila lazna uzbuna**: delovi se preklapaju pa zrak pogodi susedni deo.
  Vizuelno su normale uglavnom ispravne.
- `recalc_face_normals` je POGORSAO: celo bure okrenuto unutra (inward 7 086 -> 9 802). Zato je `repair(recalc=False)` podrazumevano.
- Mera zrakom (neparan broj pogodaka = unutra) radi na nivou ostrva, ali ne i po facama: grupe face-ova "unutra" su
  zapravo udubljenja i zlebovi, njihovo okretanje je razbilo model. Nemoj okretati po facama na osnovu zraka.
- `fix_normals_raycast(obj)` okrece samo cela ostrva koja su vecinski unutra. Na ovom modelu: 0 od 39 ostrva, pa nista ne menja (tacno).
- Zakrpe po doslednosti smera + glasanje zrakom: okrenuto samo 89 face-ova, crveni trouglovi na poklopcu su ostali.
- Preostali crveni trouglovi na poklopcu sanduka su **rupe** (granica petlji 12-36 ivica), kroz koje se vidi unutrasnja strana.
  `repair(hole_sides=32)` ih ne zatvara pouzdano (levi sanduk: 27 granicnih ivica ostalo). Treba ih zatvoriti ili ponovo napraviti rucno po delu.
- Zakljucak: automatika brise degenerisane face i zatvara deo manjih rupa (1 180 -> 516 otvorenih ivica), ali ne popravlja
  prave greske u orijentaciji ni vece rupe. Za to treba rebuild po delovima (cilindar/kutija iz primitiva), a ne popravka mreze.
