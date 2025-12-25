"""PS1 Character Generator add-on entry point."""
from __future__ import annotations

import bpy

from .ops import CLASSES as OP_CLASSES
from .ui import CLASSES as UI_CLASSES, register_properties, unregister_properties

bl_info = {
    "name": "PS1 Character Generator",
    "author": "Keegan + Codex",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar",
    "category": "Object",
}


def register():
    register_properties()
    for cls in OP_CLASSES + UI_CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(OP_CLASSES + UI_CLASSES):
        bpy.utils.unregister_class(cls)
    unregister_properties()


if __name__ == "__main__":
    register()
