# Pravila verifikacije (Dejanova dopuna, vazi za svaki Blender zadatak)

Izvor: iskustva korisnika (HN, blog o Opusu i pogresnoj verziji Blendera). Render zna da izgleda ispravno dok je geometrija pokvarena.

## 1. Meri, ne gledaj samo
Posle svake vece izmene pozovi `diagnose(obj)` iz `tripo-cleanup/tripo_cleanup.py`:
`exec(open(r"C:/Users/dejan/.claude/skills/tripo-cleanup/tripo_cleanup.py").read())`
Proveri: `nonmanifold_edges`, `zero_area_faces`, `duplicate_verts`, `loose_*`, `ngons`, `negative_scale`, `dims`.
Slika (`look`) je potrebna, ali nikad nije jedini dokaz. Kad se broj i slika ne slazu, istrazi pre nego sto nastavis.

## 2. API pre koda
Verziju Blendera procitaj iz `get_addon_status` (`blender_version`), ne pretpostavljaj.
Za svaki bpy poziv u kom nisi 100% siguran koristi `bpy_api_lookup` / `describe_node_type`.
Nodovi i enumi se trazi po tipu, nikad po imenu. Ne pisi API iz secanja za Blender 5.x (mnogo je promenjeno).
Modifajer koji ne menja viewport (Solidify i slicni) proveri brojem face-ova/dimenzija, ne okom.

## 3. Topologija i budzet
Cilj: quad-dominantna mreza, bez n-gonova na krivinama, bez trouglova na deformabilnim delovima.
Pre rada reci budzet poligona (vidi `polycount-budgets.md`); posle rada uporedi stvarni broj sa budzetom.
Nikad ne predaj model koji je samo grupa primitiva bez bevela, ako tip modela trazi detalj.

## 4. Petlja rada
modeluj -> `diagnose` -> `look` iz 3/4, spreda, sa strane i wireframe -> popravi -> ponovi.
Zavrsi sa `qa-review` verdiktom (SHIP / SHIP WITH NOTES / NO-SHIP) i navedi brojeve pre/posle.

## 5. Sigurnost
Radi na kopiji ili sacuvaj .blend pre velikih izmena. Ne brisi objekte koje nisi napravio bez pitanja.
Jedan MCP server na portu 9876 u isto vreme.
