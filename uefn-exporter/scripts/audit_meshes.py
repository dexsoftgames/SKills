# Lists every static mesh under a content folder whose SOURCE geometry (LOD 0 mesh description) is over
# the UEFN limits: 30,000 triangles or 20,000 vertices (Dejan 30.9 / 13.10.2026). Run in the source UE project
# before ExportToUEFN; afterwards each listed mesh must appear in Report.txt as Mesh.Simplified (Fixed).
# Usage (ue-mcp run_python_file): args = ["/Game/<PackFolder>"]
import sys
import unreal

root = sys.argv[1] if len(sys.argv) > 1 else "/Game"
registry = unreal.AssetRegistryHelpers.get_asset_registry()
flt = unreal.ARFilter(package_paths=[root], recursive_paths=True, class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "StaticMesh")])
over = []
for data in registry.get_assets(flt):
    mesh = data.get_asset()
    try:
        desc = mesh.get_static_mesh_description(0)
        tris = desc.get_triangle_count() if desc else mesh.get_num_triangles(0)
    except Exception:
        tris = mesh.get_num_triangles(0)
    verts = mesh.get_num_vertices(0)
    if tris > 30000 or verts > 20000:
        over.append((tris, verts, str(data.package_name)))
over.sort(reverse=True)
print("AUDIT %d meshes over the limits under %s" % (len(over), root))
for tris, verts, name in over:
    print("AUDIT %8d tris %8d verts  %s" % (tris, verts, name))
