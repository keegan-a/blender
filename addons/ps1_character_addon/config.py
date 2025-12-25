"""Configuration schemas for PS1 character generation.

This module defines lightweight data contracts shared across the add-on
so that each agent can pass information clearly to the next stage.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CharacterConfig:
    """User-facing character options.

    Attributes:
        name: Name of the character/mesh object.
        height: Target character height in Blender units.
        poly_density: Resolution preset controlling subdivisions.
        texture_size: Square texture resolution (64/128/256).
        quantize_vertices: Whether to snap vertices to a grid.
        quantize_step: Grid size used when quantizing.
    """

    name: str = "PSX_Character"
    height: float = 1.7
    poly_density: str = "LOW"
    texture_size: int = 128
    quantize_vertices: bool = True
    quantize_step: float = 0.01


@dataclass
class ReferenceSet:
    """Container for reference image filepaths."""

    body_front: Optional[str] = None
    body_back: Optional[str] = None
    body_left: Optional[str] = None
    body_right: Optional[str] = None
    face_front: Optional[str] = None
    face_profile_left: Optional[str] = None
    face_profile_right: Optional[str] = None


@dataclass
class GenerationResult:
    """Outputs created by the pipeline."""

    mesh_object_name: str
    armature_object_name: Optional[str] = None
    material_name: Optional[str] = None
    texture_image_name: Optional[str] = None
