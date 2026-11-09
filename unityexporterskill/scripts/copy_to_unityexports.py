# Copies the working Unity project into UnityExports\<Name> with nothing outside it:
#   python copy_to_unityexports.py <LevelFolderInAssets> [ExportName]
# 1. robocopy Assets, Packages, ProjectSettings (mirror)
# 2. every reference into the importer package -> the level's own copy of the same file
#    (Assets/<Level>/Source/**/<same file name>), in scenes, prefabs, materials, assets
# 3. the two packages that live on L: (importer, cinematic recorder) removed from manifest + lock
# 4. proof: 0 package references and 0 L: paths left
import os, re, sys, json, subprocess

SRC = r'H:/UnrealToUnityExporter/UnityProject'
level = sys.argv[1]
name = sys.argv[2] if len(sys.argv) > 2 else level
DST = r'H:/UnrealToUnityExporter/UnityExports/' + name
EXTERNAL = ['com.dexsoft.import-unreal-scene', 'com.dexsoft.cinematic-recorder']
YAML = ('.unity', '.prefab', '.mat', '.asset', '.lighting', '.controller', '.terrainlayer', '.preset')

for d in ('Assets', 'Packages', 'ProjectSettings'):
    rc = subprocess.call(['robocopy', os.path.join(SRC, d), os.path.join(DST, d), '/MIR', '/R:1', '/W:1',
                          '/NFL', '/NDL', '/NJH', '/NJS', '/NP'], stdout=subprocess.DEVNULL)
    if rc >= 8:
        sys.exit(f'robocopy {d} failed ({rc})')

def guid_of(meta):
    m = re.search(r'^guid: ([0-9a-f]{32})', open(meta, encoding='utf-8', errors='ignore').read(), re.M)
    return m.group(1) if m else None

cache = os.path.join(SRC, 'Library', 'PackageCache')
pkg = [d for d in os.listdir(cache) if d.startswith('com.dexsoft.import-unreal-scene@')][0]
pkg_files = {}
for root, _, fs in os.walk(os.path.join(cache, pkg)):
    for f in fs:
        if f.endswith('.meta'):
            g = guid_of(os.path.join(root, f))
            if g: pkg_files[g] = f[:-5]

level_src = os.path.join(DST, 'Assets', level, 'Source')
by_name = {}
for root, _, fs in os.walk(level_src):
    for f in fs:
        if f.endswith('.meta'):
            g = guid_of(os.path.join(root, f))
            if g: by_name.setdefault(f[:-5], g)
remap = {g: by_name[n] for g, n in pkg_files.items() if n in by_name}

changed = 0
for root, _, fs in os.walk(os.path.join(DST, 'Assets')):
    for f in fs:
        if not f.endswith(YAML):
            continue
        p = os.path.join(root, f)
        s = open(p, encoding='utf-8', errors='ignore', newline='').read()
        t = s
        for a, b in remap.items():
            if a in t:
                t = t.replace(a, b)
        if t != s:
            open(p, 'w', encoding='utf-8', newline='').write(t)
            changed += 1

for fn in ('manifest.json', 'packages-lock.json'):
    p = os.path.join(DST, 'Packages', fn)
    d = json.load(open(p, encoding='utf-8'))
    for k in EXTERNAL:
        d['dependencies'].pop(k, None)
    open(p, 'w', encoding='utf-8').write(json.dumps(d, indent=2) + '\n')
for f in os.listdir(os.path.join(DST, 'Packages')):
    if '.bak' in f:
        os.remove(os.path.join(DST, 'Packages', f))

left = lpaths = 0
for root, _, fs in os.walk(DST):
    for f in fs:
        if f.endswith(YAML) or f.endswith('.json'):
            t = open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
            if any(g in t for g in pkg_files):
                left += 1
                print('  still references the package:', os.path.relpath(os.path.join(root, f), DST))
            if 'L:/8TB' in t or 'DEXSOFT Plugins' in t:
                lpaths += 1
print(f'{DST}: {changed} file(s) rewritten, package refs left {left}, L: paths left {lpaths}')
