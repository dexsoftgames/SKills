"""Tripo/AI mesh dijagnoza i popravka u Blenderu (bmesh, bez bpy.ops osim importa).

Upotreba unutar Blendera (MCP execute_blender_code ili Script editor):
    exec(open(r"C:/Users/dejan/.claude/skills/tripo-cleanup/tripo_cleanup.py").read())
    for o in selected_meshes(): print(diagnose(o))
    for o in selected_meshes(): print(repair(o))

Headless test:
    blender -b --python tripo_cleanup.py -- model.fbx [out.fbx]
"""
import bpy, bmesh, sys
from mathutils import Vector


def selected_meshes():
    objs = [o for o in bpy.context.selected_objects if o.type == "MESH"]
    return objs or [o for o in bpy.context.scene.objects if o.type == "MESH"]


def _islands(bm):
    seen, n = set(), 0
    for f in bm.faces:
        if f.index in seen:
            continue
        n += 1
        stack = [f]
        seen.add(f.index)
        while stack:
            cur = stack.pop()
            for e in cur.edges:
                for nf in e.link_faces:
                    if nf.index not in seen:
                        seen.add(nf.index)
                        stack.append(nf)
    return n


def diagnose(obj, area_eps=1e-10):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    for i, f in enumerate(bm.faces):
        f.index = i
    d = Vector(obj.dimensions)
    r = {
        "name": obj.name,
        "dims": tuple(round(x, 4) for x in d),
        "verts": len(bm.verts), "faces": len(bm.faces),
        "tris": sum(1 for f in bm.faces if len(f.verts) == 3),
        "quads": sum(1 for f in bm.faces if len(f.verts) == 4),
        "ngons": sum(1 for f in bm.faces if len(f.verts) > 4),
        "boundary_edges": sum(1 for e in bm.edges if len(e.link_faces) == 1),
        "nonmanifold_edges": sum(1 for e in bm.edges if len(e.link_faces) > 2),
        "loose_verts": sum(1 for v in bm.verts if not v.link_edges),
        "loose_edges": sum(1 for e in bm.edges if not e.link_faces),
        "zero_area_faces": sum(1 for f in bm.faces if f.calc_area() < area_eps),
        "islands": _islands(bm),
        "uv_layers": len(obj.data.uv_layers),
        "materials": len(obj.data.materials),
        "negative_scale": any(s < 0 for s in obj.scale),
    }
    # duplikati (na 1e-5)
    seen, dup = {}, 0
    for v in bm.verts:
        k = (round(v.co.x, 5), round(v.co.y, 5), round(v.co.z, 5))
        dup += k in seen
        seen[k] = 1
    r["duplicate_verts"] = dup
    bm.free()
    return r


def repair(obj, merge_dist=1e-4, hole_sides=0, min_island_faces=0, recalc=False):
    """Redom: merge by distance -> obrisi lose delove -> degenerisane face ->
    (opciono) zatvori rupe -> normale napolje. Vraca log sa brojevima pre/posle.
    recalc=False (default): bmesh recalc_face_normals na otvorenim Tripo mrezama zna da okrene ceo deo
    POGRESNO (izmereno: bure postalo celo okrenuto unutra) - koristi fix_normals_raycast.
    hole_sides=0 (default): rupe se NE zatvaraju, jer su otvorene ivice na Tripo
    modelima uglavnom sesovi izmedju delova. Zatvaraj sa hole_sides=8..64 samo na
    delovima gde je rupa stvarna greska (selektuj taj objekat/deo)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    log = {"name": obj.name, "faces_before": len(bm.faces)}
    n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=merge_dist)
    log["merged_verts"] = n0 - len(bm.verts)
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context="EDGES")
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_edges], context="VERTS")
    zero = [f for f in bm.faces if f.calc_area() < 1e-10]
    if zero:
        bmesh.ops.delete(bm, geom=zero, context="FACES")
    log["zero_faces_removed"] = len(zero)
    # sitni odvojeni delovi (opciono)
    if min_island_faces:
        seen, rm = set(), []
        for f in bm.faces:
            if f in seen:
                continue
            isl, stack = [], [f]
            seen.add(f)
            while stack:
                c = stack.pop(); isl.append(c)
                for e in c.edges:
                    for nf in e.link_faces:
                        if nf not in seen:
                            seen.add(nf); stack.append(nf)
            if len(isl) < min_island_faces:
                rm += isl
        if rm:
            bmesh.ops.delete(bm, geom=rm, context="FACES")
        log["small_island_faces_removed"] = len(rm)
    b0 = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    if hole_sides:
        bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if len(e.link_faces) == 1], sides=hole_sides)
    log["boundary_before"] = b0
    log["boundary_after"] = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(obj.data)
    obj.data.update()
    log["faces_after"] = len(bm.faces)
    bm.free()
    return log


def fix_normals_raycast(obj, maxhits=12, flip_threshold=0.5, per_face_threshold=None):
    """Orijentacija normala po merenju, ne po topologiji. Za svako povezano ostrvo
    baci zrak iz svake face duz normale: neparan broj pogodaka = normala gleda unutra.
    Ako je udeo 'unutra' u ostrvu > flip_threshold, cele ostrvo se okrece.
    (bmesh recalc_face_normals na otvorenim/isprepletenim Tripo mrezama zna da okrene ceo deo pogresno.)
    per_face_threshold (npr. 0.8): dodatno okrece pojedinacne face tek ako je ostrvo
    gotovo sve unutra/napolje; podrazumevano iskljuceno jer unutrasnje face deluju kao greska.
    Vraca (inward_pre, inward_post, flipped_islands, total_faces)."""
    from mathutils.bvhtree import BVHTree
    bm = bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
    for i, f in enumerate(bm.faces): f.index = i
    wm = obj.matrix_world
    verts_w = [wm @ v.co for v in bm.verts]
    tree = BVHTree.FromPolygons(verts_w, [[v.index for v in f.verts] for f in bm.faces])

    def inward(f):
        if f.calc_area() < 1e-10: return None
        n = (wm.to_3x3() @ f.normal).normalized()
        cur = wm @ f.calc_center_median() + n * 1e-4; hits = 0
        for _ in range(maxhits):
            loc, nrm, idx, dist = tree.ray_cast(cur, n)
            if loc is None: break
            hits += 1; cur = loc + n * 1e-4
        return hits % 2 == 1

    state = {f.index: inward(f) for f in bm.faces}
    pre = sum(1 for v in state.values() if v)
    seen, islands = set(), []
    for f in bm.faces:
        if f.index in seen: continue
        st, isl = [f], []; seen.add(f.index)
        while st:
            c = st.pop(); isl.append(c)
            for e in c.edges:
                for nf in e.link_faces:
                    if nf.index not in seen: seen.add(nf.index); st.append(nf)
        islands.append(isl)
    flipped = 0
    for isl in islands:
        vals = [state[f.index] for f in isl if state[f.index] is not None]
        if vals and sum(vals) / len(vals) > flip_threshold:
            for f in isl: f.normal_flip()
            flipped += 1
            for f in isl:
                if state[f.index] is not None: state[f.index] = not state[f.index]
    post = sum(1 for v in state.values() if v)
    bm.to_mesh(obj.data); obj.data.update(); bm.free()
    return pre, post, flipped, len(islands)


def _main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if not argv:
        return
    src = argv[0]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ext = src.lower().rsplit(".", 1)[-1]
    if ext == "fbx": bpy.ops.import_scene.fbx(filepath=src)
    elif ext in ("glb", "gltf"): bpy.ops.import_scene.gltf(filepath=src)
    elif ext == "obj": bpy.ops.wm.obj_import(filepath=src)
    for o in selected_meshes():
        print("DIAG ", diagnose(o))
        print("REPAIR", repair(o))
        print("AFTER", diagnose(o))
    if len(argv) > 1:
        bpy.ops.export_scene.fbx(filepath=argv[1], use_selection=False)


if __name__ == "__main__" or "--" in sys.argv:
    _main()
