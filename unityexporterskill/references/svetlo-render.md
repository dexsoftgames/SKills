# Svetlo, render, ekspozicija, bake

## URP / renderer (importer ga postavlja sam — Dejan: svaki paket odmah ovako)
- Linear, HDR, MSAA Disabled (TAA Very High na kameri), Color Grading HDR + LUT 32.
- Shadow Distance 200, 4 kaskade (0.07, 0.20, 0.47), main light shadow 8192, additional lights atlas 8192 (MAX), nivoi Low/Medium/High 1024/2048/4096, Soft High, bias 1/1.
- Light Probe System: Adaptive Probe Volumes.
- Renderer **Forward+** (obavezno; Forward ima 4 svetla po objektu). Features: SSAO (0.5 / radius 0.5 / direct 0.1, falloff 100, blue noise, depth normals, High) + Decal.
- Static: sve OSIM Batching Static (instancing). Kamera izuzeta.
- Kamera: FOV 90 UVEK, post on, TAA; FlyCamera Speed 1 UVEK (28.10.).

## Lighting asset / bake
- `Dexsoft_Lighting.lighting` u Source/Settings: 4096, Default-HighResolution, 128/2048 uzoraka; uvoz i meni ga MORAJU snimiti zajedno sa scenom. Ako scena izgubi referencu, vraća se POSTOJEĆI asset.
- Baked GI on, peku se samo probe (0 lightmap atlasa), Indirect Only, Realtime GI off, AO max distance 0.5. Svi MeshRenderer Receive GI = Light Probes; sva svetla Mixed.
- Spoljni nivo sa terenom: objekti < 1 m i vegetacija bez Contribute GI (TooSmallOrGreenForGi), lokalni APV samo preko terena+modela bez fill empty, baking set 3/81 m. Broj uzoraka po tipu nivoa (otvoren = manje, enterijer = više).
- Bake: zatvori Unreal (VRAM). Ne diraj Unity dok traje.

## Ekspozicija (ODOBRENO 25.9.)
- Post Exposure = Unrealova ekspozicija − log2(pojačanje svetala) + ExposureLift 1.33. Svetlina se štimuje SAMO kroz Post Exposure, nikad Ambient Intensity.
- Tonemapping ACES, Contrast 14, Saturation 10, Bloom 1.0/0.35/0.7, Vignette 0.22/0.45 (sunčane scene).
- Dnevno nebo Dexsoft/Sky: _Exposure = boost × 0.51, ambient = proizvod/(boost×0.51).
- Noć sa ručnom ekspozicijom: `environment.manualExposure`, NormalizeExposure se preskače; nebo prati jačinu meseca.
- Bez sunca/SkyLight/HDRI (enterijer): nema neba, ambijent/refleksije crni, ekspozicija po Unrealu (metered interior: tačne candele, Unity post = bias − minEV − log2(π) + 0.51).
- Unity ne pregradi ambient probe kad se skybox dodeli iz skripte → `DynamicGI.UpdateEnvironment()`.
- `VolumeProfile.Add<T>()` ne upisuje komponentu u asset → uvek `UnrealRenderSetup.ProfileComponent<T>`.

## Sobe i lokalni PP
- Automatske sobe ISKLJUČENE (Harbour: 4334 „sobe" ispod stena). Sobe se prave RUČNO u Unrealu kao bounded PostProcessVolume → `environment.localPostProcess` → `PV_Local_<ime>` sa profilom `Source/PostProcessing/PP_Local_*.asset`.
- Harbour barn (ODOBRENO): Manual, Exposure Bias 2.5, Leaking 0.2, Indirect 1.5, prio 1, blend 300 cm; u Unity-ju Dejan ručno 3.5 post exposure.
- Enterijer bez landscape-a i bez otvorenog neba → JEDNA box sonda preko nivoa.
- Sonde: jedna glavna + par na glavnom delu; Unrealove capture-e kopiraj (zakopan capture se diže na pod).

## Magla
- Visinska: `environment.heightFog` (Unrealovi brojevi; gustina = FogDensity/1000 po cm). Volume-domen meševi = lokalna volumetrijska magla (`fogVolumes` + atlas 3D šuma) → DexsoftVolumetricFogFeature. Unity fog se tada gasi.

## Nebo (dnevno)
- HDRI iz Unreala pobeđuje (kopira se fajl, ne konvertuje). Inače Dexsoft/Sky (tri ravni oblaka, ODOBRENO 25.9: Coverage 0.302, Density 3.23, Octaves 2, Scale 0.00022).
- Sky dome mesh (> 10 km) se nikad ne izvozi kao mesh. Unrealova kupola M_Sky_Panning_Clouds2 → skybox, vidi nebo-cestice-voda-vegetacija.md.
