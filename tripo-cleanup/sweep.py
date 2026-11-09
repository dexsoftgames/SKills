"""Headless sweep: dijagnoza svih FBX/GLB u folderu. Upotreba:
blender -b --python sweep.py -- <folder> <out.json>
"""
import bpy, bmesh, sys, os, json, glob
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tripo_cleanup.py"), encoding="utf-8").read().split("def _main")[0])

def extra(obj):
    bm = bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
    before = [f.normal.copy() for f in bm.faces]
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    flipped = sum(1 for f, n in zip(bm.faces, before) if f.normal.dot(n) < 0)
    # mali odvojeni delovi (plutajuce krpice)
    seen, sizes = set(), []
    for f in bm.faces:
        if f in seen: continue
        st, c = [f], 0; seen.add(f)
        while st:
            x = st.pop(); c += 1
            for e in x.edges:
                for nf in e.link_faces:
                    if nf not in seen: seen.add(nf); st.append(nf)
        sizes.append(c)
    tiny = sum(1 for s in sizes if s < 30)
    elen = [e.calc_length() for e in bm.edges]
    long_ratio = (max(elen) / (sum(elen) / len(elen))) if elen else 0
    bm.free()
    return {"flipped_faces": flipped, "tiny_islands": tiny, "max_edge_over_mean": round(long_ratio, 1)}

argv = sys.argv[sys.argv.index("--") + 1:]
folder, out = argv[0], argv[1]
files = sorted(glob.glob(os.path.join(folder, "**", "*.fbx"), recursive=True) + glob.glob(os.path.join(folder, "**", "*.glb"), recursive=True))
res = []
for fp in files:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        if fp.lower().endswith(".fbx"): bpy.ops.import_scene.fbx(filepath=fp)
        else: bpy.ops.import_scene.gltf(filepath=fp)
    except Exception as ex:
        res.append({"file": fp, "error": str(ex)}); continue
    for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
        d = diagnose(o); d.update(extra(o)); d["file"] = os.path.relpath(fp, folder); res.append(d)
json.dump(res, open(out, "w"), indent=1)
print("SWEEP_DONE", len(files), len(res))
