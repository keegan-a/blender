# PS1 Character Add-on – Agents

This document defines the agents and responsibilities for building a Blender add-on that can:

- Ingest front/back/side reference images (face + full body)
- Generate a low-poly, PS1-style character mesh
- Create PS1-appropriate UVs and textures
- Auto-rig the character for animation
- Expose the whole pipeline through a Blender add-on UI

The goal is to keep each concern isolated and hand off clean, well-defined artifacts between agents.

---

## Global Goals & Constraints

- **Target Style:** PlayStation 1 / late-90s 3D (low poly, visible edges, crunchy textures).
- **Poly Budget:** Approx. 1.5k–3k triangles for a typical humanoid.
- **Textures:**
  - Texture atlases of 64×64, 128×128, or 256×256.
  - No normal maps; just color maps (optionally alpha).
  - Pixel-art style painting, nearest-neighbor filtering.
- **Automation:** Minimal user steps – user provides reference images and basic parameters, add-on does the rest.
- **Determinism:** Same inputs → same result. Avoid randomization except where explicitly allowed.

---

## Pipeline Overview

1. **Coordinator** gathers requirements and constraints.
2. **Spec & Data Agent** defines input schema (refs, options) and output schema (mesh, armature, materials).
3. **Reference Image Agent** validates and aligns reference images in Blender.
4. **Modeling Agent** generates a PS1-style low-poly base mesh.
5. **PS1 Style Agent** enforces style constraints (poly count, hard edges, quantization).
6. **UV Agent** unwraps and packs a PS1-style atlas.
7. **Texture Agent** sets up materials, texture atlases, and optional helper textures.
8. **Rigging Agent** builds a simple humanoid rig with weights.
9. **Add-on Engineer** implements the Blender add-on, operators, and UI.
10. **QA Agent** tests the end-to-end workflow inside Blender.
11. **Docs Agent** writes user-facing docs and examples.

Each agent’s output becomes the next agent’s input.

---

## Agent: Coordinator

**Role**  
Own the high-level vision and keep all agents aligned with the PS1 character goal.

**Responsibilities**

- Define the overall pipeline and file layout.
- Ensure all agents use shared naming conventions and schemas.
- Resolve conflicts and keep scope realistic for a single add-on.

**Inputs**

- User requirements (PS1 style, refs, rig expectations).
- Blender version and environment constraints.

**Outputs**

- Finalized pipeline overview (this document).
- Shared constants (poly budget, texture sizes, default settings).
- Project folder structure (mirrors the directory structure on `D:\`).

**Handoffs**

- Provides constraints to all other agents.
- Receives feedback from QA & Add-on Engineer and updates this spec.

---

## Agent: Spec & Data Schema

**Role**  
Formalize data contracts: what goes in, what comes out of each stage.

**Responsibilities**

- Define how reference images are specified:
  - Filepaths, roles (`face_front`, `body_left`, etc.), and optional camera calibration.
- Define configurable options:
  - Height, head/body proportions, poly density presets, texture size preset.
- Define output structure:
  - Naming for objects (`CHAR_Mesh`, `CHAR_Armature`), vertex group naming, material naming.
- Define internal data:
  - Custom properties on objects for re-running or updating the pipeline.

**Inputs**

- Coordinator’s constraints.
- User expectations for how they want to interact with the add-on.

**Outputs**

- Structured schemas (e.g. Python dataclasses / dictionaries) for:
  - `CharacterConfig`
  - `ReferenceSet`
  - `GenerationResult`
- Clear comments the Add-on Engineer can copy directly into code.

**Handoffs**

- Provides schemas to all agents.
- Ensures all later agents share a consistent understanding of input/output.

---

## Agent: Reference Image Processor

**Role**  
Validate, categorize, and set up reference images in Blender.

**Responsibilities**

- Validate that all required reference slots are filled or gracefully fall back:
  - Minimum: `body_front`, `body_side`.
  - Optional: back, mirrored sides, face close-ups.
- Generate a simple viewport setup:
  - Planes or empties with reference images for front/side/back views.
  - Lock transforms / collections to avoid accidental editing.
- Optionally compute approximate real-world scale from user input (height).

**Inputs**

- `ReferenceSet` (file paths + roles).
- `CharacterConfig` (height, scale presets).

**Outputs**

- Blender objects/collections:
  - `REF_Images` collection with planes/empties.
- A simple data structure for other agents:
  - Camera alignment info or bounding boxes from refs.

**Handoffs**

- Passes reference planes and metadata to the Modeling Agent.

---

## Agent: Modeling & Topology (Base Mesh)

**Role**  
Create a low-poly humanoid mesh suitable for PS1 style, using refs as a guide.

**Responsibilities**

- Create a parametric base mesh (male/female/neutral sliders optional later, but base must be robust).
- Project silhouette and proportions to roughly match front & side refs.
- Preserve topology that plays well with animation:
  - Edge loops around joints.
  - Minimal but clean geometry (no ngons).
- Keep triangle budget within defined limits.

**Inputs**

- Reference setup (from Reference Agent).
- `CharacterConfig` poly density preset and proportions.

**Outputs**

- A single mesh object:
  - Name: `CHAR_Mesh` (or configurable prefix).
  - Clean topology: mostly quads, easy to triangulate.
- Optionally store parameters as custom properties for future regeneration.

**Handoffs**

- Passes mesh to PS1 Style Agent for style enforcement.
- Feeds into UV and Rigging Agents later.

---

## Agent: PS1 Style Enforcer

**Role**  
Make the mesh look/behave like a PS1 model.

**Responsibilities**

- Triangulate mesh or ensure consistent triangulation (while keeping a Quad edit version if needed).
- Optional vertex position quantization:
  - e.g., snap vertices to a low-resolution grid to simulate fixed-point precision.
- Control smoothing:
  - Mostly flat shading, deliberate hard edges.
- Enforce limits:
  - Max vertices/polys.
  - Max number of materials on the mesh (ideally 1–2).

**Inputs**

- `CHAR_Mesh` from Modeling Agent.
- PS1 style constraints from Coordinator.

**Outputs**

- Final game-style mesh object:
  - Name: `CHAR_Mesh_PSX`.
  - All transforms applied.
  - Consistent triangulation.

**Handoffs**

- Sends the PSX mesh to UV Agent.
- Rigging Agent also uses this mesh.

---

## Agent: UV & Atlas Generator

**Role**  
Create PS1-style UVs and pack them into a small texture atlas.

**Responsibilities**

- Generate simple UV seams:
  - Torso shells, limb shells, head shell.
- Use a limited texture size (e.g. 128×128 by default).
- Pack UV islands efficiently while preserving pixel-grid alignment.
- Optionally add pixel snap:
  - Align UV borders to integer texel units.

**Inputs**

- `CHAR_Mesh_PSX` mesh.
- Texture size preset and UV options from `CharacterConfig`.

**Outputs**

- UV map (named `UV_Atlas`) on the mesh.
- Metadata describing which regions correspond to which body parts (optional).

**Handoffs**

- Provides UV data to Texture Agent.
- Exposes atlas sizes/options to UI via Add-on Engineer.

---

## Agent: Texture & Material Setup

**Role**  
Create the PS1-style material and blank atlas, ready for pixel art.

**Responsibilities**

- Create a single material for the character:
  - Name: `MAT_PSX_Character`.
  - Simple Principled BSDF or Emission with a single image texture node.
- Create a new image texture:
  - 64/128/256 square; alpha optional.
  - Set interpolation to **Closest** (nearest neighbor).
- Assign the material to `CHAR_Mesh_PSX`.
- Optionally:
  - Generate helper layers (wireframe overlay, body-part guideline textures).

**Inputs**

- UV’d mesh (`CHAR_Mesh_PSX` + `UV_Atlas`).
- Texture size from UV Agent / Config.

**Outputs**

- Material datablock.
- Image datablock (texture atlas).
- Correct assignment to mesh.

**Handoffs**

- Texture can be painted manually by user or by future auto-texturing logic.
- Mesh/material combination passed to Rigging Agent and QA Agent.

---

## Agent: Rigging & Skinning

**Role**  
Build a simple humanoid armature and bind the mesh.

**Responsibilities**

- Create a basic biped armature:
  - Spine, head/neck, shoulders, arms, hands, legs, feet.
- Generate bones based on mesh proportions (use bounding boxes & reference markers).
- Parent mesh to armature with either:
  - Automatic weights, then
  - Optional clean-up: limit max influences, normalize weights.
- Set up basic bone names compatible with common rigging conventions.

**Inputs**

- Final PSX mesh (`CHAR_Mesh_PSX`).
- Optional config for number of spine bones, limb length ratios.

**Outputs**

- Armature object: `CHAR_Armature`.
- Mesh parented and skinned to armature.
- Vertex groups aligned to bone names.

**Handoffs**

- QA Agent uses this to validate pose and deformation.
- Add-on Engineer exposes rig generation controls in the UI.

---

## Agent: Blender Add-on Engineer

**Role**  
Turn all of the above logic into a robust Blender add-on.

**Responsibilities**

- Add-on structure:
  - `bl_info`, registration, panels, operators, and preferences.
  - Keep everything in a single Python package with clear modules:
    - `refs.py`, `modeling.py`, `psx_style.py`, `uvs.py`, `textures.py`, `rig.py`, `ui.py`, `ops.py`.
- Implement operators:
  - `PSXCHAR_OT_import_refs`
  - `PSXCHAR_OT_generate_base_mesh`
  - `PSXCHAR_OT_apply_psx_style`
  - `PSXCHAR_OT_generate_uvs`
  - `PSXCHAR_OT_setup_texture`
  - `PSXCHAR_OT_rig_character`
  - `PSXCHAR_OT_run_full_pipeline`
- Build UI panel (e.g. in 3D View > N-Panel > “PS1 Character”):
  - Input fields for reference image paths.
  - Presets for poly density and texture size.
  - Buttons for each pipeline stage + a “One-Click Generate” button.

**Inputs**

- All previous design decisions and schemas.
- Blender API & version constraints.

**Outputs**

- Fully functional add-on that can be installed via `Edit > Preferences > Add-ons > Install…`
- Clear error reporting and user feedback.

**Handoffs**

- Hands add-on to QA Agent.
- Hands usage info to Docs Agent.

---

## Agent: QA & Test Scenarios

**Role**  
Test the add-on end-to-end and verify that each stage works and fails gracefully.

**Responsibilities**

- Define test cases:
  - Minimum refs (just front/side body).
  - Full set of refs (front/back/sides, face close-ups).
  - Missing or invalid image paths.
  - Extremely tall/short characters, different proportions.
- Validate outputs:
  - Check for non-manifold geometry, UV overlap (optional), weird weights.
- Confirm PS1 style constraints are being respected.

**Inputs**

- Installed add-on in Blender.
- Example reference image sets stored in the project folder.

**Outputs**

- QA notes and bug reports.
- Suggestions for UI tweaks and error messages.

**Handoffs**

- Feedback loop into Coordinator and Add-on Engineer.

---

## Agent: Documentation & Examples

**Role**  
Create user-facing documentation and example files.

**Responsibilities**

- Write `README.md` with:
  - Installation steps.
  - Basic “Generate Character from Refs” tutorial.
  - Known limitations and troubleshooting.
- Provide example reference image sets in `/assets/refs`.
- Provide simple `.blend` files showing:
  - Generated PS1 character.
  - Rigged and posed example.

**Inputs**

- Final add-on behavior.
- QA findings.

**Outputs**

- `README.md`, animated GIFs/screenshots (optional).
- Example `.blend` and reference image folders.

**Handoffs**

- Used by future contributors and end users.
- Serves as reference for extending the add-on.

---
