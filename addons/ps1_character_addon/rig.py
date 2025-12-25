"""Simple humanoid rig creation."""
from __future__ import annotations

import bpy
from mathutils import Vector

from .config import CharacterConfig
from .utils import log


def _add_bone(armature, name, head, tail, parent=None):
    bone = armature.edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    if parent:
        bone.parent = parent
    return bone


def create_humanoid_rig(mesh_obj: bpy.types.Object, config: CharacterConfig) -> bpy.types.Object:
    """Create a lightweight biped armature and skin the mesh."""
    if mesh_obj is None:
        raise ValueError("Mesh object is required for rigging")

    log("Creating humanoid rig")

    arm_data = bpy.data.armatures.new("CHAR_Armature")
    arm_obj = bpy.data.objects.new("CHAR_Armature", arm_data)
    bpy.context.scene.collection.objects.link(arm_obj)

    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')

    bbox = mesh_obj.bound_box
    min_z = min(v[2] for v in bbox)
    max_z = max(v[2] for v in bbox)
    mid_x = sum(v[0] for v in bbox) / 8
    mid_y = sum(v[1] for v in bbox) / 8

    pelvis = _add_bone(arm_data, "pelvis", Vector((mid_x, mid_y, min_z + config.height * 0.45)), Vector((mid_x, mid_y, min_z + config.height * 0.5)))
    spine = _add_bone(arm_data, "spine", pelvis.tail, pelvis.tail + Vector((0, 0, config.height * 0.25)), pelvis)
    neck = _add_bone(arm_data, "neck", spine.tail, spine.tail + Vector((0, 0, config.height * 0.05)), spine)
    head = _add_bone(arm_data, "head", neck.tail, neck.tail + Vector((0, 0, config.height * 0.1)), neck)

    def limb(side: str, axis: float, up: float, length: float, parent_bone):
        upper = _add_bone(
            arm_data,
            f"{side}_upper",
            parent_bone.head + Vector((axis, 0, up)),
            parent_bone.head + Vector((axis, 0, up + length * 0.5)),
            parent_bone,
        )
        lower = _add_bone(
            arm_data,
            f"{side}_lower",
            upper.tail,
            upper.tail + Vector((axis, 0, length * 0.5)),
            upper,
        )
        _add_bone(
            arm_data,
            f"{side}_end",
            lower.tail,
            lower.tail + Vector((axis, 0, length * 0.2)),
            lower,
        )

    limb("arm.L", config.height * 0.12, pelvis.head.z - min_z, config.height * 0.4, spine)
    limb("arm.R", -config.height * 0.12, pelvis.head.z - min_z, config.height * 0.4, spine)
    limb("leg.L", config.height * 0.08, 0.0, config.height * 0.45, pelvis)
    limb("leg.R", -config.height * 0.08, 0.0, config.height * 0.45, pelvis)

    bpy.ops.object.mode_set(mode='OBJECT')

    mesh_obj.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    log("Rig created and mesh skinned")
    return arm_obj
