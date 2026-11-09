# Materijali i teksture

## Pravila za teksture (Dejan 9.10. i 16.10.2026 — GLAVNA)
1. Svaka tekstura `T_...`, nikad `MI_...`. Izvedena tekstura se zove po IZVORNOJ teksturi (`T_<ime>_MetallicSmoothness`, `_Occlusion`, `_rot90`...).
2. Bilo šta u alfi → **TGA**, ne PNG.
3. ARM/ORM se nikad ne preskače → uvek `T_<ime>_MetallicSmoothness.tga`.
4. Identične teksture (isti pikseli) = jedan fajl; identični materijali = jedan materijal (ostala imena preusmerena u manifestu). Posle toga DRUGA nezavisna provera heševima; ako i dalje ima duplikata — spoji i javi glasno.

## PBR — tri slučaja, BEZ pogađanja (ResolvePbrByRule, 5.10.2026)
1. ARM/MasterPainter (`T_*_OcclusionRoughnessMetallic`, `_ARM`, `_ORM`, param npr. `AORoughnessMetallicTexture`) = **R AO / G rough / B metal UVEK** (po imenu teksture; ne pogađati kanale pikselima za imenovan ARM — sjajni sto je ispao crn).
   - R → `Occlusion.png`; 255−G → alfa `MetallicSmoothness.tga`; B → RGB (metal).
   - `metallicTexEnabled` isključen → RGB = skalar `metallic`, fajl `_M<xx>`.
   - Množioci mastera se primenjuju (skalar Rough+Mult/Scale množi G, Metal+Mult/Scale množi B) → sufiks `_R200`/`_MM018`.
   - Placeholder mastera (T_checkboard) po imenu parametra se ne uzima.
2. MR master (posebne Metallic i Roughness mape) → MetallicSmoothness. `*_Metallic` mape u Dexsoft paketima su već Unity MetallicSmoothness (alfa = smoothness) ako nema roughness mape.
3. Samo skalari → brojevi u manifest → Unity klizači, bez teksture.
- ARM/metal/rough/AO i maske slojeva terena (ORD/ORM) se čitaju SIROVO (LoadAsRawBGRA8, bez sRGB→linear). Kolor/normal kroz Adjustments (AdjustImageColors).
- Kad je graf pročitan: mape iz analize grafa (tačna formula). Pravila po imenu samo kad graf nije pročitan.
- UV rotacija (mainTexRotation, četvrtine) se peče u teksture `_rot90/180/270` + tiling/offset (Unity Lit nema rotaciju).
- Statički prekidač u MASTERU (`normalMapTexEnabled` false...) odseca mapu i u Unrealu → export je tada tačan. Ne juriti override kvačice na instanci.
- Boje: Unreal linearno → `.gamma` za SetColor, clamp 0..1, bez „dizanja" tinta. Emission takođe `.gamma` (bez toga 5 → 34).

## Emisija
- Glow = boja × mapa; crna mapa u slotu (T_black) = nema glow-a. Switch sa „Emissi" u imenu ima poslednju reč.
- 28.10.: kad nijedan vektor ne nosi „Emissi/Glow" u imenu, a postoji imenovana jačina (Glow/Emissive skalar), boja = vektor-parametar koji graf zaista vodi u Emissive pin (iskre M_MagicSpark: Color × Glow 6).

## UV drift (klizanje teksture)
- Brzina iz Panner čvora (sa smerom) ima prednost; po imenu („Speed"/„Pan") samo kao rezerva.
- 28.10.: parametar koji graf vodi SAMO u World Position Offset (npr. `SpeedWave` na M_MasterMainWave — talasanje platna) NIJE drift (OnlyMovesVertices). Platno na kutijama ostaje običan URP Lit, bez vetra.
- `DexsoftUvDrift` radi preko MaterialPropertyBlock (nikad kopija materijala — ranije su kutije posle reload-a ostajale roze).
- Providna površina sa driftom ≥ 0.05 UV/s + normal mapom = tekuća voda (bFlowing).

## Tečnost (kazan, 28.10.2026) — Dexsoft/AnimatedLiquid
Prepoznaje se strukturom: Emissive povezan, BaseColor = Lerp(VectorParam, VectorParam, TextureSample sa Panner koordinatama), Time u grafu. Čita: deep/bright boje, masku + kanal, normal (panneri), WorldPosition tile (cm→m), Flow, Pulse (sin, amplituda/bias sa čvorova posle Sine), EmissiveStrength, Roughness. ResolveLiquid se zove i na „by-name" putu (materijal bez teksture boje uvek ide tim putem).

## Staklo — ODOBRENO 25.9.2026, NE DIRATI
Preset `M_DexsoftGlass.mat` klonira se po slotu, prepisuje se samo `_BaseColor` (ako tint nije beo ni CRN) i `_Cull`. Vrednosti: FresnelAlphaInfluence 0.585, FresnelPower 1.6, Smoothness 0.957, ReflectionStrength 1.12, RefractionStrength 0.019, AmbientStrength 1.46, tint (0.5258, 0.5269, 0.5283). Crni tint iz Unreala se NE upisuje. URP: `m_OpaqueDownsampling = 0`, `m_RequireOpaqueTexture = true`. Staklo ne Contribute GI. APV vidljivo ne menja GI kroz staklo — Dejan: „batali".

## Teren
- SVI slojevi mat (`maskMapRemapMax.w = 0.05`), osim imena sa wet/puddle/mokr (ODOBRENO 16.10.). Negativan *SPEC u landscape masteru = matte.
- Tiling slojeva se piše na tri načina (UVScale funkcija / LandscapeLayerCoords / TexCoord×'Layer UV Scale'); LandscapeLayerCoords **deli** (Scale = 1/MappingScale).
- WorldAlignedBlend unutar funkcije jedne površine = triplanar, ne auto-materijal. MatLayerBlend u jednom paint layeru → SplitBlendedPaintLayers.
- Neprečitano: hue/desaturation čvorovi posle teksture (foliage) se još ne peku po instanci.
