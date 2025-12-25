"""UV generation for PS1-style atlas."""
from __future__ import annotations

import bpy

from .utils import log


def generate_psx_uvs(mesh_obj: bpy.types.Object, texture_size: int) -> None:
    """Create UVs with basic seams and packing."""
    if mesh_obj is None:
        raise ValueError("Mesh object is required for UV generation")

    log("Generating UVs")
    bpy.context.view_layer.objects.active = mesh_obj

    uv_layer = mesh_obj.data.uv_layers.get("UV_Atlas")
    if uv_layer is None:
        uv_layer = mesh_obj.data.uv_layers.new(name="UV_Atlas")
    mesh_obj.data.uv_layers.active = uv_layer

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=1.0 / texture_size)
    bpy.ops.uv.pack_islands(rotate=False, margin=1.0 / texture_size)
    bpy.ops.object.mode_set(mode='OBJECT')

    log("UVs generated and packed")
