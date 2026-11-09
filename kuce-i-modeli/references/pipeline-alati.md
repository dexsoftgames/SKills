# Pipeline i alati (putanje na Dejanovom glavnom računaru)

## Novi modeli („pravimo nove modele")

Ceo dogovoreni postupak (Gemini scena → grid objekata → seckanje → Tripo → Maya → Painter → export → Unreal) je u
`H:\IzradaModela\pipeline\pipeline.py` — pročitaj ga PRVO. Po modelu: `run_model.py maya` / `finish <plan.json>`.
Tripo delovi: bez QuadRemeshera, samo čišćenje non-manifold (Maya `polyCleanupArgList`, razdvoji verteksе).

## Gde je šta

| Šta | Putanja |
|---|---|
| Kuće (kombinator) | `E:\!Share\MedVillMegaFIN\HouseBuilder\assemble_houses.py` |
| Krovovi | `E:\!Share\MedVillMegaFIN\RoofLibrary\make_roof_frames.py` |
| Daske/grede | `E:\!Share\MedVillMegaFIN\PlankLibrary\make_planks.py` |
| Zidni moduli | `E:\!Share\MedVillMegaFIN\WallLibrary\make_walls.py` |
| Podovi | `E:\!Share\MedVillMegaFIN\FloorLibrary\` |
| Delovi kuća (okviri, vrata) | `E:\!Share\MedVillMegaFIN\HouseParts\` |
| Nameštaj/propsi | `E:\!Share\MedVillMegaFIN\Props\Chairs\` (`make_chairs.py`, `rebuild_set.sh <SET>`, `make_narrow.py`) |
| UV alati | `E:\Tripo\uv_unfold.py`, `E:\Tripo\uvpack80.py` |
| Painter most | `E:\Tripo\painter_do.py` (startup modul `claude_bridge.py` u Painteru) |
| GENERIC / šavovi | `E:\Tripo\generic\`, `E:\Tripo\stitches\` |
| Unreal projekat sela | `E:\!Share\MedVillMegaFIN\MedVillMegaFIN.uproject` (mapa MedievalVillage3) |

## Zamke

- Maya: commandPort `:7001` (Dejan ga otvara ručno). Kad Dejan ne može da objasni → otvori mu model u Mayi i uporedi verteksе.
- UE Python preko mosta: izlaz u fajl (log puca >90 KB); dug sken (15k aktera) ruši editor → u delovima po ~1500.
- Nikad `load_level` u Python-u preko mosta, nikad `EditorAssetLibrary.rename_asset`.
- bmesh `faces.new` ne računa normalu → `normal_update()` + `ngon_method='BEAUTY'`.
- `bpy.data.libraries.load` mutira listu imena → dodeli `list(names)`.
- `me.materials.clear()` resetuje material_index → sačuvaj i vrati indekse.
- FBX iz Blendera u UE preslikava Y/X: proveri pivot i yaw (kuće: actor na (W,0), yaw 180).
