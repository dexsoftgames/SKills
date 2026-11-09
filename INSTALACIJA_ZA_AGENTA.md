# Uputstvo za agenta: instaliraj Dejanova 3 Claude skilla na ovaj računar

Ti si Claude Code na novom računaru. Tvoj zadatak je da na ovaj računar instaliraš tri Dejanova skilla, tako da
Claude odmah zna njegova pravila. Uradi sve sam, korak po korak, i posle svakog koraka pokreni njegovu proveru.
Dejanu odgovaraj na srpskom, kratko. Na kraju mu pošalji izveštaj (korak 6).

| Skill | Za šta |
|---|---|
| `kuce-i-modeli` | izrada srednjovekovnih kuća, ambara, nameštaja i propsa (Blender → UV → Substance Painter → Unreal) |
| `unityexporterskill` | Dexsoft exporter „Export Scene To Unity" (Unreal 5.8 → Unity 6 URP) |
| `uefn-exporter` | Dexsoft exporter „Export To UEFN" (Unreal 5.8 → UEFN/Fortnite) |

Izvor: privatni GitHub repo **https://github.com/dexsoftgames/SKills.git** (grana `main`, ime sa velikim K).
Odredište: **`%USERPROFILE%\.claude\skills`**. Taj folder JESTE git repo; Claude Code odatle sam čita skillove.

## Pravila

- Ne briši nijedan postojeći folder u `%USERPROFILE%\.claude\skills`. Tamo mogu biti drugi skillovi (npr. `synced\` ili
  Blender paket) koji nisu u repou i moraju ostati. Repo ih ne dira, jer je njegov `.gitignore` bela lista sa samo 3 skilla.
- Ne unosi lozinku ni token za GitHub. Prijavu radi Dejan sam u prozoru koji Git otvori (korak 2).
- Ne pravi commit i ne radi push sa ovog računara, osim ako Dejan to izričito traži.
- Ništa ne menjaj u samim skillovima. Ako nešto ne odgovara ovom računaru (drugo slovo diska), zapiši to u izveštaj.

## 1. Git

```powershell
git --version
```
Ako git ne postoji: instaliraj ga (`winget install --id Git.Git -e --source winget`, ili instaler iz
`L:\8TB\DEXSOFT Plugins\SVIMCPSERVERI\Installers\` ako je taj disk dostupan), pa otvori nov PowerShell.
**Provera:** `git --version` ispisuje verziju.

## 2. Prijava na GitHub (repo je privatan)

```powershell
git ls-remote https://github.com/dexsoftgames/SKills.git main
```
Ako iskoči prozor „Connect to GitHub", reci Dejanu: „Prijavi se na GitHub nalog dexsoftgames u prozoru koji je otvoren
(Sign in with your browser)". Sačekaj da kaže da je gotovo i ponovi komandu. Git Credential Manager posle pamti prijavu.
**Provera:** komanda ispiše jedan red sa hešom i `refs/heads/main`.

## 3. Preuzimanje repoa u folder skillova

```powershell
$S = Join-Path $env:USERPROFILE ".claude\skills"
if (-not (Test-Path $S)) {
    git clone https://github.com/dexsoftgames/SKills.git $S
} elseif (-not (Test-Path (Join-Path $S ".git"))) {
    # Folder vec postoji (npr. od instalera): repo se dodaje u njega, nista postojece se ne brise
    git -C $S init -b main
    git -C $S remote add origin https://github.com/dexsoftgames/SKills.git
    git -C $S fetch origin main
    git -C $S checkout -f -B main --track origin/main
} else {
    git -C $S pull origin main
}
```
Ako `checkout` javi da bi prepisao postojeće fajlove istog imena (npr. stara kopija `uefn-exporter`), to je u redu:
`-f` ih menja verzijom iz repoa, koja je glavna. Drugi folderi ostaju netaknuti.

**Provera:**
```powershell
foreach ($k in 'kuce-i-modeli','unityexporterskill','uefn-exporter') {
    "{0,-20} {1}" -f $k, (Test-Path (Join-Path $S "$k\SKILL.md"))
}
git -C $S status -sb
```
Sva tri moraju biti `True`, a `status` mora pokazati `## main...origin/main` bez izmena.

## 4. Provera da Claude Code vidi skillove

Pokreni nov Claude Code chat (stari ne vidi nove skillove). U listi dostupnih skillova moraju biti
`kuce-i-modeli`, `unityexporterskill` i `uefn-exporter`. Probaj i `/kuce-i-modeli`: treba da učita pravila za kuće.

## 5. Šta skillovi traže na disku (samo proveri i zapiši, ne kopiraj ništa sam)

Skill nosi pravila, ali alati i projekti moraju postojati na istim putanjama kao na Dejanovom glavnom računaru.
Proveri svaku putanju sa `Test-Path` i zapiši DA/NE:

| Skill | Putanje |
|---|---|
| `kuce-i-modeli` | `E:\Tripo\` (painter_do.py, generic\, stitches\, uv_unfold.py, uvpack80.py), `H:\IzradaModela\pipeline\pipeline.py`, `E:\!Share\MedVillMegaFIN\HouseBuilder\` |
| `unityexporterskill` | `H:\UnrealToUnityExporter\`, `H:\UTUB\`, `L:\8TB\DEXSOFT Plugins\` |
| `uefn-exporter` | `H:\UnrealToUEFN\`, `L:\8TB\DEXSOFT Plugins\UnrealPlugins\UnrealToUEFN_UE5.8_Win64\` |
| zajedničko | UE 5.8: `J:\EpicGamesDownloadFiles\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` (ili gde god je 5.8 instaliran), UEFN: `C:\Program Files\Epic Games\Fortnite\FortniteGame\Binaries\Win64\UnrealEditorFortnite-Win64-Shipping.exe`, Blender, Substance 3D Painter, Unity 6 |

Ako Unreal 5.8 postoji, a `L:\8TB` je dostupan, Dejan može da pokrene
`L:\8TB\DEXSOFT Plugins\UnrealPlugins\UnrealToUEFN_UE5.8_Win64\Install.bat` za UEFN plugin.
Ti to pokreni SAMO ako Dejan kaže, i samo dok nijedan Unreal editor ne radi.

## 6. Izveštaj Dejanu (na srpskom)

1. Da li su sva 3 skilla instalirana (provera iz koraka 3 i 4).
2. Tabela iz koraka 5: šta postoji, a šta fali na ovom računaru.
3. Šta si još menjao ili instalirao (npr. git).

## Kasnije: osvežavanje

Kad Dejan na glavnom računaru izmeni skill i pushuje, ovde je dovoljno:
```powershell
git -C (Join-Path $env:USERPROFILE ".claude\skills") pull origin main
```
pa nov Claude Code chat.
