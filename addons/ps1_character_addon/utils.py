"""Shared utility helpers for the PS1 character add-on."""
from __future__ import annotations

import bpy


def log(message: str) -> None:
    """Lightweight console logger for debugging."""
    print(f"[PSX_CHAR] {message}")


def get_or_create_collection(name: str) -> bpy.types.Collection:
    """Return an existing collection or create a new one at the scene root."""
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    return collection


def get_object(name: str) -> bpy.types.Object | None:
    """Safely fetch an object by name."""
    return bpy.data.objects.get(name)


def apply_object_transforms(obj: bpy.types.Object) -> None:
    """Apply location, rotation, and scale transforms for a given object."""
    if obj is None:
        return
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
