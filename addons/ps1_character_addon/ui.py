"""UI definitions for the PS1 character add-on."""
from __future__ import annotations

import bpy

from .ops import (
    PSXCHAR_OT_apply_psx_style,
    PSXCHAR_OT_generate_base_mesh,
    PSXCHAR_OT_generate_uvs,
    PSXCHAR_OT_import_refs,
    PSXCHAR_OT_rig_character,
    PSXCHAR_OT_run_full_pipeline,
    PSXCHAR_OT_setup_texture,
)


def register_properties():
    scene = bpy.types.Scene

    scene.psx_body_front_path = bpy.props.StringProperty(name="Body Front", subtype='FILE_PATH')
    scene.psx_body_back_path = bpy.props.StringProperty(name="Body Back", subtype='FILE_PATH')
    scene.psx_body_left_path = bpy.props.StringProperty(name="Body Left", subtype='FILE_PATH')
    scene.psx_body_right_path = bpy.props.StringProperty(name="Body Right", subtype='FILE_PATH')
    scene.psx_face_front_path = bpy.props.StringProperty(name="Face Front", subtype='FILE_PATH')
    scene.psx_face_profile_left_path = bpy.props.StringProperty(name="Face Left", subtype='FILE_PATH')
    scene.psx_face_profile_right_path = bpy.props.StringProperty(name="Face Right", subtype='FILE_PATH')

    scene.psx_character_name = bpy.props.StringProperty(name="Name", default="PSX_Character")
    scene.psx_character_height = bpy.props.FloatProperty(name="Height", default=1.7, min=0.5, max=3.0)
    scene.psx_poly_density = bpy.props.EnumProperty(
        name="Poly Density",
        items=[("LOW", "Low", ""), ("MEDIUM", "Medium", ""), ("HIGH", "High", "")],
        default="LOW",
    )
    scene.psx_texture_size = bpy.props.EnumProperty(
        name="Texture Size",
        items=[("64", "64", ""), ("128", "128", ""), ("256", "256", "")],
        default="128",
    )
    scene.psx_quantize_vertices = bpy.props.BoolProperty(name="Quantize Vertices", default=True)
    scene.psx_quantize_step = bpy.props.FloatProperty(name="Quantize Step", default=0.01, min=0.001, max=0.1)


def unregister_properties():
    props = [
        "psx_body_front_path",
        "psx_body_back_path",
        "psx_body_left_path",
        "psx_body_right_path",
        "psx_face_front_path",
        "psx_face_profile_left_path",
        "psx_face_profile_right_path",
        "psx_character_name",
        "psx_character_height",
        "psx_poly_density",
        "psx_texture_size",
        "psx_quantize_vertices",
        "psx_quantize_step",
    ]
    for prop in props:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)


class VIEW3D_PT_ps1_character(bpy.types.Panel):
    bl_label = "PS1 Character"
    bl_idname = "VIEW3D_PT_ps1_character"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PS1 Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Reference Images")
        box.prop(scene, "psx_body_front_path")
        box.prop(scene, "psx_body_back_path")
        box.prop(scene, "psx_body_left_path")
        box.prop(scene, "psx_body_right_path")
        box.prop(scene, "psx_face_front_path")
        box.prop(scene, "psx_face_profile_left_path")
        box.prop(scene, "psx_face_profile_right_path")
        box.operator(PSXCHAR_OT_import_refs.bl_idname, text="Refresh References")

        box = layout.box()
        box.label(text="Character Settings")
        box.prop(scene, "psx_character_name")
        box.prop(scene, "psx_character_height")
        box.prop(scene, "psx_poly_density")
        box.prop(scene, "psx_texture_size")
        box.prop(scene, "psx_quantize_vertices")
        box.prop(scene, "psx_quantize_step")

        box = layout.box()
        box.label(text="Pipeline")
        box.operator(PSXCHAR_OT_import_refs.bl_idname, text="Import Refs")
        box.operator(PSXCHAR_OT_generate_base_mesh.bl_idname, text="Generate Base Mesh")
        box.operator(PSXCHAR_OT_apply_psx_style.bl_idname, text="Apply PSX Style")
        box.operator(PSXCHAR_OT_generate_uvs.bl_idname, text="Generate UVs")
        box.operator(PSXCHAR_OT_setup_texture.bl_idname, text="Setup Texture")
        box.operator(PSXCHAR_OT_rig_character.bl_idname, text="Rig Character")
        box.operator(PSXCHAR_OT_run_full_pipeline.bl_idname, text="Generate Full PS1 Character")


CLASSES = [VIEW3D_PT_ps1_character]
