# Lists every asset name under a content folder, grouped by class, so the names can be spell-checked by eye
# before ExportToUEFN (Dejan 16.10.2026: misspellings and Serbian names are fixed in the SOURCE project first,
# with the rename keeping every connection). Usage (ue-mcp run_python_file): args = ["/Game/<PackFolder>"]
import sys
import unreal
root = sys.argv[1] if len(sys.argv) > 1 else "/Game"
reg = unreal.AssetRegistryHelpers.get_asset_registry()
names = {}
for d in reg.get_assets_by_path(root, recursive=True):
    if str(d.asset_class_path.asset_name) in ("World", "MapBuildDataRegistry"):
        continue
    names.setdefault(str(d.asset_class_path.asset_name), []).append(str(d.asset_name))
for cls in sorted(names):
    print("NAMES %s (%d): %s" % (cls, len(names[cls]), " ".join(sorted(names[cls]))))
