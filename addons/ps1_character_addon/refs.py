"""Reference image setup utilities."""
from __future__ import annotations

import math
from pathlib import Path

import bpy

from .config import ReferenceSet
from .utils import get_or_create_collection, log

REF_COLLECTION = "REF_Images"


def _clear_ref_collection(collection: bpy.types.Collection) -> None:
    """Remove all objects from the reference collection."""
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def _load_image(path: str) -> bpy.types.Image | None:
    file_path = Path(path)
    if not file_path.exists():
        log(f"Reference not found: {file_path}")
        return None
    existing = bpy.data.images.get(file_path.name)
    if existing:
        return existing
    try:
        return bpy.data.images.load(str(file_path))
    except RuntimeError:
        log(f"Failed to load image: {file_path}")
        return None


def _create_image_empty(name: str, image: bpy.types.Image, location: tuple[float, float, float], rotation: tuple[float, float, float]) -> bpy.types.Object:
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = 'IMAGE'
    obj.data = image
    obj.empty_image_depth = 'FRONT'
    obj.empty_display_size = 1.0
    obj.image_user.frame_start = 1
    obj.image_user.use_auto_refresh = True
    obj.location = location
    obj.rotation_euler = rotation
    obj.lock_location = (True, True, True)
    obj.lock_rotation = (True, True, True)
    obj.lock_scale = (True, True, True)
    return obj


def setup_reference_images(refs: ReferenceSet) -> None:
    """Create image empties for provided reference images.

    Safe to call multiple times – the REF_Images collection is cleared
    before new empties are created.
    """

    collection = get_or_create_collection(REF_COLLECTION)
    _clear_ref_collection(collection)

    mapping = {
        "body_front": ((0.0, -1.0, 0.0), (math.radians(-90), 0.0, 0.0)),
        "body_back": ((0.0, 1.0, 0.0), (math.radians(-90), 0.0, math.pi)),
        "body_left": ((-1.0, 0.0, 0.0), (math.radians(-90), 0.0, math.radians(90))),
        "body_right": ((1.0, 0.0, 0.0), (math.radians(-90), 0.0, math.radians(-90))),
        "face_front": ((0.0, -0.5, 1.6), (math.radians(-90), 0.0, 0.0)),
        "face_profile_left": ((-0.5, 0.0, 1.6), (math.radians(-90), 0.0, math.radians(90))),
        "face_profile_right": ((0.5, 0.0, 1.6), (math.radians(-90), 0.0, math.radians(-90))),
    }

    for slot, transform in mapping.items():
        path = getattr(refs, slot)
        if not path:
            continue
        image = _load_image(path)
        if image is None:
            continue
        location, rotation = transform
        obj = _create_image_empty(f"REF_{slot}", image, location, rotation)
        collection.objects.link(obj)

    log("Reference images refreshed.")
