"""Operators driving the PS1 character pipeline."""
from __future__ import annotations

import bpy

from .config import CharacterConfig, ReferenceSet
from .modeling import create_base_character_mesh
from .psx_style import apply_psx_style
from .refs import setup_reference_images
from .rig import create_humanoid_rig
from .textures import setup_psx_material
from .uvs import generate_psx_uvs
from .utils import get_object, log


def _config_from_scene(scene: bpy.types.Scene) -> CharacterConfig:
    return CharacterConfig(
        name=scene.psx_character_name or "PSX_Character",
        height=scene.psx_character_height,
        poly_density=scene.psx_poly_density,
        texture_size=int(scene.psx_texture_size),
        quantize_vertices=scene.psx_quantize_vertices,
        quantize_step=scene.psx_quantize_step,
    )


def _refs_from_scene(scene: bpy.types.Scene) -> ReferenceSet:
    return ReferenceSet(
        body_front=scene.psx_body_front_path,
        body_back=scene.psx_body_back_path,
        body_left=scene.psx_body_left_path,
        body_right=scene.psx_body_right_path,
        face_front=scene.psx_face_front_path,
        face_profile_left=scene.psx_face_profile_left_path,
        face_profile_right=scene.psx_face_profile_right_path,
    )


class PSXCHAR_OT_import_refs(bpy.types.Operator):
    bl_idname = "psxchar.import_refs"
    bl_label = "Import Reference Images"
    bl_description = "Load reference images into the scene"

    def execute(self, context):
        refs = _refs_from_scene(context.scene)
        setup_reference_images(refs)
        self.report({'INFO'}, "References refreshed")
        return {'FINISHED'}


class PSXCHAR_OT_generate_base_mesh(bpy.types.Operator):
    bl_idname = "psxchar.generate_base_mesh"
    bl_label = "Generate Base Mesh"
    bl_description = "Create the low-poly base character mesh"

    def execute(self, context):
        config = _config_from_scene(context.scene)
        mesh_obj = create_base_character_mesh(config)
        mesh_obj.name = "CHAR_Mesh"
        self.report({'INFO'}, "Base mesh generated")
        return {'FINISHED'}


class PSXCHAR_OT_apply_psx_style(bpy.types.Operator):
    bl_idname = "psxchar.apply_psx_style"
    bl_label = "Apply PSX Style"
    bl_description = "Triangulate and quantize the mesh"

    def execute(self, context):
        mesh_obj = get_object("CHAR_Mesh")
        if mesh_obj is None:
            self.report({'ERROR'}, "No CHAR_Mesh found")
            return {'CANCELLED'}
        config = _config_from_scene(context.scene)
        apply_psx_style(mesh_obj, config)
        self.report({'INFO'}, "PSX style applied")
        return {'FINISHED'}


class PSXCHAR_OT_generate_uvs(bpy.types.Operator):
    bl_idname = "psxchar.generate_uvs"
    bl_label = "Generate UVs"
    bl_description = "Create PS1-friendly UVs"

    def execute(self, context):
        mesh_obj = get_object("CHAR_Mesh")
        if mesh_obj is None:
            self.report({'ERROR'}, "No CHAR_Mesh found")
            return {'CANCELLED'}
        config = _config_from_scene(context.scene)
        generate_psx_uvs(mesh_obj, config.texture_size)
        self.report({'INFO'}, "UVs generated")
        return {'FINISHED'}


class PSXCHAR_OT_setup_texture(bpy.types.Operator):
    bl_idname = "psxchar.setup_texture"
    bl_label = "Setup Texture"
    bl_description = "Create PSX material and texture"

    def execute(self, context):
        mesh_obj = get_object("CHAR_Mesh")
        if mesh_obj is None:
            self.report({'ERROR'}, "No CHAR_Mesh found")
            return {'CANCELLED'}
        config = _config_from_scene(context.scene)
        setup_psx_material(mesh_obj, config.texture_size)
        self.report({'INFO'}, "Texture and material ready")
        return {'FINISHED'}


class PSXCHAR_OT_rig_character(bpy.types.Operator):
    bl_idname = "psxchar.rig_character"
    bl_label = "Rig Character"
    bl_description = "Create a simple humanoid rig and skin the mesh"

    def execute(self, context):
        mesh_obj = get_object("CHAR_Mesh")
        if mesh_obj is None:
            self.report({'ERROR'}, "No CHAR_Mesh found")
            return {'CANCELLED'}
        config = _config_from_scene(context.scene)
        create_humanoid_rig(mesh_obj, config)
        self.report({'INFO'}, "Rig created")
        return {'FINISHED'}


class PSXCHAR_OT_run_full_pipeline(bpy.types.Operator):
    bl_idname = "psxchar.run_full_pipeline"
    bl_label = "Generate Full PS1 Character"
    bl_description = "Run all stages: refs, mesh, style, UVs, textures, rig"

    def execute(self, context):
        scene = context.scene
        refs = _refs_from_scene(scene)
        config = _config_from_scene(scene)

        setup_reference_images(refs)
        mesh_obj = create_base_character_mesh(config)
        mesh_obj.name = "CHAR_Mesh"
        apply_psx_style(mesh_obj, config)
        generate_psx_uvs(mesh_obj, config.texture_size)
        setup_psx_material(mesh_obj, config.texture_size)
        create_humanoid_rig(mesh_obj, config)

        self.report({'INFO'}, "Full PSX character generated")
        return {'FINISHED'}


CLASSES = [
    PSXCHAR_OT_import_refs,
    PSXCHAR_OT_generate_base_mesh,
    PSXCHAR_OT_apply_psx_style,
    PSXCHAR_OT_generate_uvs,
    PSXCHAR_OT_setup_texture,
    PSXCHAR_OT_rig_character,
    PSXCHAR_OT_run_full_pipeline,
]
