# Renames assets by NAME under a content root with Unreal's AssetTools (references are updated, redirectors are left
# for fixup_redirectors). Usage (ue-mcp run_python_file): args = ["/Game/<Pack>", "OldName=NewName", ...]
# A name that matches more than one asset is skipped and reported (never guessed).
import sys
import unreal
root = sys.argv[1]
pairs = [a.split("=", 1) for a in sys.argv[2:]]
reg = unreal.AssetRegistryHelpers.get_asset_registry()
by_name = {}
for d in reg.get_assets_by_path(root, recursive=True):
    by_name.setdefault(str(d.asset_name), []).append(d)
jobs, skipped = [], []
for old, new in pairs:
    found = by_name.get(old, [])
    if len(found) != 1:
        skipped.append("%s (%d matches)" % (old, len(found)))
        continue
    d = found[0]
    folder = str(d.package_path)
    jobs.append(unreal.AssetRenameData(d.get_asset(), folder, new))
ok = unreal.AssetToolsHelpers.get_asset_tools().rename_assets(jobs) if jobs else True
print("RENAME %d requested, ok=%s, skipped: %s" % (len(jobs), ok, skipped))
