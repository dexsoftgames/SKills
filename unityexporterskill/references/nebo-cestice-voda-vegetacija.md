# Noćno nebo, čestice, rotatori, voda, vegetacija

## Noćno nebo — Unrealova kupola → Dexsoft/PanningCloudSky (Witch House 28.10.2026, ODOBRENO)
- Exporter: kupola (> 10 km) sa materijalom porodice M_Sky_Panning_Clouds2 (parametri Zenith Color, Horizon color, Light direction, Sun Radius) → manifest `skyDome` (sve boje, sunce/mesec, zvezde, oblaci, panneri, yaw aktera, teksture T_Sky_Clouds_M / T_Sky_Blue / T_Sky_Stars pisane direktno, iako su /Engine/).
- Šejder prepisuje graf čvor po čvor u Unreal osama. UV sfere SM_SkySphere izmereni: UV0 u = 0.75 − az/360, v = 1 − |el|/90; UV1 polarno po hemisferi. Mesec = SphereMask(dot(CameraVector, LightDir), 1, SunRadius), hardness 0.
- **Zvezde PROCEDURALNE** (StarLayer, tačke veličine piksela, treperenje) — T_Sky_Stars 512 px daje mrlje; Dejan ih je dvaput odbio.
- **Odobrene noćne vrednosti** (UnrealSkyPlacer Night* konstante, važe kad je najjači kanal zenita < 0.05; boje, mesec i pravac iz Unreala):
  Exposure 0.74, HorizonFalloff 0.5, NoisePower1 0.25, NoisePower2 2.2, StarsBrightness 0.05, SunHeight 2.89, StarBoost 0.36, CloudOpacity 1.33, CloudSpeed 0.23, CloudPan 0.01, BluePan 1.25, Yaw −51.55, SunBrightness 4, SunRadius 0.0025.
- Materijal `Assets/<P>/Source/Materials/SkyDome.mat`; šejder se kopira u `Source/Shaders` (menjati i tu kopiju).

## Niagara → Unity Particle System (28.10.2026)
- Exporter (NiagaraExporter.cpp): po sistemu emiteri sa modulima po fazama (EmitterSpawn/Update, ParticleSpawn/Update), ulazi `{v}`/`{s}`/dinamički `{fn,inputs}`/krive `{curve}`; RapidIterationParameters „Constants.<Emitter>.<Module>.<Input>"; redosled modula šetnjom parameter-map pinova; renderi sprite (tekstura čestice evaluirana boja+opacity, subImages), mesh (FBX), light.
- Flipbook: materijal sa `ParticleSubUV` → tekstura čestice = sam SubUV list sa alfom (inače kvadrati umesto dima).
- Importer (UnrealParticlePlacer): prefabovi u `Assets/<P>/Prefabs/Particles`, instance u grupi `Particles` — **briše svoje stare pre postavljanja** (ranije 3 uvoza = 3 kopije svakog dima). Materijali čestica se prepisuju svakim uvozom (SaveMaterial).
- Moduli: EmitterState, SpawnRate, SpawnBurst, InitializeParticle, AddVelocity, AddVectorToPosition/ShapeLocation, AccelerationForce, Gravity, Drag, CurlNoise/Wind, ScaleSprite/MeshSize, Color, ScaleColor, SubUVAnimation, Lights. Jedinice cm→m, ose Unreal→Unity.
- Emiter može biti rotiran (Witch House dim: lokalno z = gore) — „naviše" štelovati po lokalnoj osi koja gleda gore.
- U Edit modu čestice ne emituju dok se ne selektuju ili ne pusti Play.
- Witch House ručno u prefabovima (posle uvoza; ponovni uvoz ih vraća na Unreal): mehurići sporiji (VOL y 0.06–0.12, x/z ±0.03, life 2.5–4, noise 0.06/1.2/0.4); dim veći (size 0.23–0.32, life 2.2–4, VOL z 0.25–0.38).

## Rotatori (28.10.2026)
- Akter sa RotatingMovementComponent → manifest `rotators` (pivot, rotacija, rate u Unity osama: (−Pitch, Yaw, Roll), local). Importer skuplja objekte nazvane po akteru pod `<ime>_Rotator` + `DexsoftRotator` (okreće samo u Play). Witch House BookMagic: 110°/s.

## Voda (ODOBRENO 9.10. / 16.10.2026)
- Detekcija po shading modelu SingleLayerWater (pa klasa WaterBody, pa heuristika); voda izlazi iz sceneMeshes.
- Unity kači PRESET po `kind` (lake/ocean/river): ponašanje iz preseta (`M_DexsoftLake/Ocean.mat`, Dejanove vrednosti 9.10), BOJA iz Unreala (ApplyMeasuredColour: Scattering, Absorption, BaseColor, DeepColour = σs/(σs+σa), `.gamma`).
- Shore mapa se peče iz heightmape (Unity nema Distance Field); preset se bira PRE pečenja. Brzine talasa iz Panner čvorova, ne iz WaveSpeed parametara. Koeficijenti ×100 (Unreal po cm).
- `[Toggle]` iz skripte ne pali keyword — postaviti i float i keyword.

## Vegetacija (ODOBRENO)
- Biljka = slot masked && twoSided; drvo vs trava = postoji čvrst slot. List ili kora odlučuje ALFA base teksture (TGA → list).
- Trava: Dexsoft/Foliage Wind (SmallAmp −0.040, LargeAmp −0.138, tajlovi 0.30/0.63 m, PivotLock 0.69, Wiggle 0.008).
- Drveće/palme/banane: Dexsoft/Foliage Cutout (SwayAngle 1/60, SwaySpeed 0.6, SwayWave 1.0, LeafWeight 0.25 / Push 10 / Lift 1, Cull Off). WindZone 0.12 (ne dizati).
- Alfa na mipovima: mipMapsPreserveCoverage + alphaTestReferenceValue 0.3333; detail prototip koristi exportovani mesh (ne pečenu kopiju).
