# Pravi release zip na 8TB (UnrealPlugin/ + UnityPackage/ + UserGuide) iz H:/UTUB builda i kopira ga u SVIMCPSERVERI.
# Pokretati TEK posle Dejanovog odobrenja. Pre toga: pack_importer.py (tgz) i BuildPlugin u H:/UTUB.
import os, shutil, zipfile, hashlib
REL = r'L:/8TB/DEXSOFT Plugins/UnrealPlugins/UnrealToUnityExporterWithLandscape_1.0'
STAGE = REL + '/UnrealToUnityExporterWithLandscape_1.0'
BUILD = r'H:/UTUB/UnrealToUnityExporterWithLandscape'
SRC = r'H:/UnrealToUnityExporter/Plugins/UnrealToUnityExporterWithLandscape'
dst = STAGE + '/UnrealPlugin/UnrealToUnityExporterWithLandscape'
shutil.rmtree(dst)
os.makedirs(dst + '/Binaries/Win64')
for f in ('UnrealEditor-UnrealToUnityExporterWithLandscape.dll', 'UnrealEditor.modules'):
    shutil.copy2(BUILD + '/Binaries/Win64/' + f, dst + '/Binaries/Win64/' + f)
shutil.copytree(BUILD + '/Source', dst + '/Source')
shutil.copytree(SRC + '/Config', dst + '/Config')
shutil.copy2(BUILD + '/UnrealToUnityExporterWithLandscape.uplugin', dst + '/UnrealToUnityExporterWithLandscape.uplugin')
zp = REL + '/UnrealToUnityExporterWithLandscape_1.0.zip'
tmp = zp + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, fs in os.walk(STAGE):
        for f in fs:
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, STAGE).replace(chr(92), '/'))
os.replace(tmp, zp)
shutil.copy2(zp, r'L:/8TB/DEXSOFT Plugins/SVIMCPSERVERI/DexsoftPlugins/Unreal/UnrealToUnityExporterWithLandscape_1.0.zip')
z = zipfile.ZipFile(zp)
names = z.namelist()
print(len(names), 'files', os.path.getsize(zp), 'bytes')
print('pdb in zip:', any(n.endswith('.pdb') for n in names))
dll = z.read('UnrealPlugin/UnrealToUnityExporterWithLandscape/Binaries/Win64/UnrealEditor-UnrealToUnityExporterWithLandscape.dll')
print('dll matches build:', dll == open(BUILD + '/Binaries/Win64/UnrealEditor-UnrealToUnityExporterWithLandscape.dll', 'rb').read())
tgz = z.read('UnityPackage/com.dexsoft.import-unreal-scene-1.0.0.tgz')
print('tgz matches packed importer:', tgz == open(STAGE + '/UnityPackage/com.dexsoft.import-unreal-scene-1.0.0.tgz', 'rb').read())
for need in ('Source/UnrealToUnityExporterWithLandscape/Private/NiagaraExporter.cpp',):
    print(need, any(n.endswith(need) for n in names))
print('svim copy same:', open(zp,'rb').read() == open(r'L:/8TB/DEXSOFT Plugins/SVIMCPSERVERI/DexsoftPlugins/Unreal/UnrealToUnityExporterWithLandscape_1.0.zip','rb').read())
print('md5', hashlib.md5(open(zp,'rb').read()).hexdigest())
