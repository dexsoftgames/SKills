# Zamke koje su već nešto pokvarile (sa datumom)

| datum | šta se desilo | pravilo |
|---|---|---|
| 28.10.2026 | Export pokrenut dok su se šejderi kompajlirali → 64 umesto 136 modela | čekaj compiling = 0 + miran log |
| 28.10.2026 | Za vreme Dejanovog bake-a ubačen nov importer + prepisan šejder → Unity pao (D3D12 device removed), bake izgubljen | proveri Lightmapping.isRunning i isPlaying pre svake izmene |
| 28.10.2026 | Vrednosti neba upisane iz zastarelog fajla sa diska (10:19 umesto 10:49), pa onda vraćene kad nije trebalo | pitaj da li je snimljeno (Save Project), čitaj živo preko MCP-a, pokaži tabelu pre upisa |
| 28.10.2026 | 3 uvoza = 3 kopije svakog Niagara sistema (96 umesto 32) | placer briše svoju grupu pre postavljanja |
| 28.10.2026 | Materijal čestice nije osvežen ponovnim uvozom (stara tekstura bez alfe) | materijali se uvek prepisuju preko postojećeg (SaveMaterial) |
| 28.10.2026 | Scena i dalje stari šejder neba posle izmene paketa | uvoz kopira šejder u Source/Shaders — prepiši i kopiju |
| 28.10.2026 | Nova float osobina šejdera na postojećem materijalu = 0 (StarBoost) | importer postavlja svaku novu osobinu eksplicitno |
| 28.10.2026 | DexsoftUvDrift u OnDisable uništavao klon materijala → roze kutije posle reload-a | MaterialPropertyBlock, nikad klon |
| 28.10.2026 | SpeedWave (WPO talas) pročitan kao klizanje teksture platna | parametar samo u WPO nije drift |
| 28.10.2026 | Iskre tamne Lit kugle (emisija kroz Custom čvor) | boja iz vektora koji vodi u Emissive pin |
| 28.10.2026 | Tečnost kazana preskočena (ide by-name putem) | ResolveLiquid i na by-name putu |
| 28.10.2026 | Kamera prebrza: Speed po veličini nivoa, FlyCamera seče na 2 | Speed = 1 uvek |
| 28.10.2026 | Plugin van Engine\Plugins\Marketplace → pada SVAKI C++ build sa 5.8 (UE5Rules.dll) | samo Marketplace; nikad preimenovati UE5Rules.dll |
| 28.10.2026 | Ubijeni Unity Asset Import Worker procesi (mislio sam da su bake) | ne ubijati Unity procese |
| 16.10.2026 | Self-contain posle snimanja → scena bez lighting asseta → bake 1024/Medium zaglavljen | svaki korak posle snimanja sam snima |
| 19.10.2026 | Harbour bake satima pa pad drajvera (25k GI učesnika, Unreal otvoren) | sitno/vegetacija bez Contribute GI, zatvori Unreal |
| 16.10.2026 | Voda tirkizna (DeepColour nikad pisan) | boja iz Unreala, ponašanje iz preseta |
| 9.10.2026 | Teksture MI_, PNG sa alfom, preskočen ARM, duplikati | pravila za teksture |
| 5.10.2026 | Pikselna provera kanala ispremeštala ARM metalnog stola | imenovan ARM = R AO/G rough/B metal uvek |
| 26.08.2026 | AlignFbxAxes mirror (scale −1) → stepenice naopako | čist yaw −90°, bez flipa |
| 26.08.2026 | Ambient probe nula (skybox iz skripte) → crne senke | DynamicGI.UpdateEnvironment() |
| 25.9.2026 | VolumeProfile.Add ne snima komponentu | ProfileComponent<T> |
| — | JsonUtility ne ostavlja ugnježden objekat null | proveravaj polje (npr. skyDome.clouds prazno = nema) |
| — | Brisanje fajlova u korenu Assets otvara modal koji blokira MCP | briši samo foldere |
| — | Kad regresija „padne", prvo proveri da li je očekivana vrednost ispravna | 2 od 3 pada bila greška provere |

## Opšti principi
- Graf govori jasno, a čitač zna samo jedan od više načina da se to kaže → kad ne prepozna oblik, prijavi, ne vraćaj sirovinu tiho.
- „Nema u Unrealu = nema u Unity-ju" (bez sunca nema neba, itd.).
- Kad vidiš nešto sumnjivo (sRGB na data mapi...), KAŽI odmah, ne odlučuj tiho.
- Dejan ćuti = dobro; kad kaže „odlično" — stani.
