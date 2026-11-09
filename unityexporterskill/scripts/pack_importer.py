# Packs the Unity importer (com.dexsoft.import-unreal-scene) into the npm-style tgz
# Unity's Package Manager reads ("package/" prefix), straight into the 8TB release folder.
# Usage: python pack_importer.py
import os, tarfile

SRC = r'H:/UnrealToUnityExporter/Plugins/com.dexsoft.import-unreal-scene'
OUT = r'L:/8TB/DEXSOFT Plugins/UnrealPlugins/UnrealToUnityExporterWithLandscape_1.0/UnrealToUnityExporterWithLandscape_1.0/UnityPackage/com.dexsoft.import-unreal-scene-1.0.0.tgz'
SKIP_DIRS = {'.git', 'node_modules'}

tmp = OUT + '.tmp'
n = 0
with tarfile.open(tmp, 'w:gz') as tar:
    for root, dirs, files in os.walk(SRC):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            if f.endswith(('.bak', '.orig', '.tmp')):
                continue
            p = os.path.join(root, f)
            tar.add(p, arcname='package/' + os.path.relpath(p, SRC).replace(os.sep, '/'))
            n += 1
os.replace(tmp, OUT)
print(n, 'files', os.path.getsize(OUT), 'bytes ->', OUT)
