"""Procedural low-poly character generation."""
from __future__ import annotations

import bpy
from mathutils import Vector

from .config import CharacterConfig
from .utils import log


def _density_segments(poly_density: str) -> int:
    return {"LOW": 1, "MEDIUM": 2, "HIGH": 3}.get(poly_density, 1)


def create_base_character_mesh(config: CharacterConfig) -> bpy.types.Object:
    """Build a simple blocky humanoid mesh and return the object."""
    log("Creating base character mesh")
    segments = _density_segments(config.poly_density)

    mesh = bpy.data.meshes.new("CHAR_Mesh")
    obj = bpy.data.objects.new("CHAR_Mesh", mesh)
    bpy.context.scene.collection.objects.link(obj)

    verts = []
    faces = []

    height = config.height
    torso_height = height * 0.35
    leg_height = height * 0.45
    head_height = height * 0.2
    width = height * 0.18

    # Torso block
    torso_verts_start = len(verts)
    verts.extend(
        [
            Vector((-width, -width, leg_height)),
            Vector((width, -width, leg_height)),
            Vector((width, width, leg_height)),
            Vector((-width, width, leg_height)),
            Vector((-width, -width, leg_height + torso_height)),
            Vector((width, -width, leg_height + torso_height)),
            Vector((width, width, leg_height + torso_height)),
            Vector((-width, width, leg_height + torso_height)),
        ]
    )
    faces.extend([
        (torso_verts_start, torso_verts_start + 1, torso_verts_start + 2, torso_verts_start + 3),
        (torso_verts_start + 4, torso_verts_start + 5, torso_verts_start + 6, torso_verts_start + 7),
        (torso_verts_start, torso_verts_start + 1, torso_verts_start + 5, torso_verts_start + 4),
        (torso_verts_start + 1, torso_verts_start + 2, torso_verts_start + 6, torso_verts_start + 5),
        (torso_verts_start + 2, torso_verts_start + 3, torso_verts_start + 7, torso_verts_start + 6),
        (torso_verts_start + 3, torso_verts_start, torso_verts_start + 4, torso_verts_start + 7),
    ])

    # Head block
    head_size = width * 1.1
    head_z = leg_height + torso_height
    head_start = len(verts)
    verts.extend(
        [
            Vector((-head_size, -head_size, head_z)),
            Vector((head_size, -head_size, head_z)),
            Vector((head_size, head_size, head_z)),
            Vector((-head_size, head_size, head_z)),
            Vector((-head_size, -head_size, head_z + head_height)),
            Vector((head_size, -head_size, head_z + head_height)),
            Vector((head_size, head_size, head_z + head_height)),
            Vector((-head_size, head_size, head_z + head_height)),
        ]
    )
    faces.extend([
        (head_start, head_start + 1, head_start + 2, head_start + 3),
        (head_start + 4, head_start + 5, head_start + 6, head_start + 7),
        (head_start, head_start + 1, head_start + 5, head_start + 4),
        (head_start + 1, head_start + 2, head_start + 6, head_start + 5),
        (head_start + 2, head_start + 3, head_start + 7, head_start + 6),
        (head_start + 3, head_start, head_start + 4, head_start + 7),
    ])

    def add_limb(x_offset: float, y_offset: float, length: float, radius: float) -> None:
        base = len(verts)
        verts.extend(
            [
                Vector((x_offset - radius, y_offset - radius, leg_height)),
                Vector((x_offset + radius, y_offset - radius, leg_height)),
                Vector((x_offset + radius, y_offset + radius, leg_height)),
                Vector((x_offset - radius, y_offset + radius, leg_height)),
                Vector((x_offset - radius, y_offset - radius, leg_height + length)),
                Vector((x_offset + radius, y_offset - radius, leg_height + length)),
                Vector((x_offset + radius, y_offset + radius, leg_height + length)),
                Vector((x_offset - radius, y_offset + radius, leg_height + length)),
            ]
        )
        faces.extend([
            (base, base + 1, base + 2, base + 3),
            (base + 4, base + 5, base + 6, base + 7),
            (base, base + 1, base + 5, base + 4),
            (base + 1, base + 2, base + 6, base + 5),
            (base + 2, base + 3, base + 7, base + 6),
            (base + 3, base, base + 4, base + 7),
        ])

    limb_radius = width * 0.4
    arm_length = torso_height * 0.9
    leg_length = leg_height

    add_limb(-width * 1.1, 0.0, arm_length, limb_radius)
    add_limb(width * 1.1, 0.0, arm_length, limb_radius)

    add_limb(-width * 0.6, 0.0, leg_length, limb_radius)
    add_limb(width * 0.6, 0.0, leg_length, limb_radius)

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.subdivide(number_cuts=segments - 1) if segments > 1 else None
    bpy.ops.object.editmode_toggle()

    log("Base character mesh created")
    return obj
