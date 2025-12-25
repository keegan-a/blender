"""Texture and material setup for PS1 characters."""
from __future__ import annotations

import bpy

from .utils import log


def setup_psx_material(mesh_obj: bpy.types.Object, texture_size: int) -> tuple[str, str]:
    """Create a nearest-filtered material and image texture."""
    image_name = f"IMG_PSX_Character_{texture_size}"
    material_name = "MAT_PSX_Character"

    image = bpy.data.images.get(image_name)
    if image is None:
        image = bpy.data.images.new(image_name, width=texture_size, height=texture_size)

    material = bpy.data.materials.get(material_name)
    if material is None:
        material = bpy.data.materials.new(material_name)
        material.use_nodes = True

    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    tex = nodes.new(type="ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = 'Closest'
    bsdf.inputs['Specular'].default_value = 0.0

    tex.location = (-400, 0)
    bsdf.location = (-150, 0)
    output.location = (200, 0)

    links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    if mesh_obj.data.materials:
        mesh_obj.data.materials[0] = material
    else:
        mesh_obj.data.materials.append(material)

    log("Material and texture setup complete")
    return material.name, image.name
