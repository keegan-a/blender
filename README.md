# PS1 Character Generator Add-on

This repository contains a Blender 4.0+ add-on for building PlayStation 1-style characters from reference images. The add-on procedurally generates a low-poly mesh, applies PSX-era styling, unwraps UVs for a small texture atlas, and rigs the result with a simple humanoid armature. All steps can be driven from an N-panel UI, and reference images can be refreshed at any time without reinstalling the add-on.

## Installation

1. Zip the `addons/ps1_character_addon` folder or install it directly via **Edit > Preferences > Add-ons > Install...** and choose the folder.
2. Enable **PS1 Character Generator** in the add-on list.

## Usage

1. Open the 3D Viewport and expand the **N-panel**. Choose the **PS1 Tools** tab and open the **PS1 Character** panel.
2. In **Reference Images**, set any available body and face image paths. Click **Refresh References** to load/update the planes.
3. In **Character Settings**, choose a name, target height, poly density preset, texture size (64/128/256), and vertex quantization options.
4. Run individual pipeline steps or press **Generate Full PS1 Character** to execute everything: import refs, build the mesh, apply PSX style, generate UVs, create the texture/material, and build the rig.
5. To change face or outfit references later, simply update the file paths in the panel and click **Refresh References** or re-run the relevant stages—no reinstall required.

## Notes

- Generated objects are named `CHAR_Mesh` and `CHAR_Armature` for easy reuse.
- Texture images are created with nearest-neighbor filtering to preserve the crunchy pixel-art look.
- The add-on is deterministic: the same inputs and settings produce the same output.
