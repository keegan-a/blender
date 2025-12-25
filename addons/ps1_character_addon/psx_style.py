"""PS1 style enforcement utilities."""
from __future__ import annotations

import bpy

from .config import CharacterConfig
from .utils import log


def apply_psx_style(mesh_obj: bpy.types.Object, config: CharacterConfig) -> bpy.types.Object:
    """Triangulate, quantize vertices, and set flat shading."""
    if mesh_obj is None:
        raise ValueError("Mesh object is required")

    log("Applying PSX styling")
    bpy.context.view_layer.objects.active = mesh_obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    if config.quantize_vertices:
        step = config.quantize_step
        for vert in mesh_obj.data.vertices:
            vert.co.x = round(vert.co.x / step) * step
            vert.co.y = round(vert.co.y / step) * step
            vert.co.z = round(vert.co.z / step) * step

    for face in mesh_obj.data.polygons:
        face.use_smooth = False

    if len(mesh_obj.material_slots) > 1:
        mesh_obj.active_material_index = 0
        while len(mesh_obj.material_slots) > 1:
            bpy.ops.object.material_slot_remove()

    log("PSX styling applied")
    return mesh_obj
