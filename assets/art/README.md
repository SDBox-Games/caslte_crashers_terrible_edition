# Editable runtime art

Every PNG below is loaded by the game at startup. Static artwork uses a centered
transparent canvas so it can be repainted without changing gameplay anchors.

Animated actors live in `rigs/<actor>/`. Each has independently editable PNGs in
`parts/` and an `animation.json`. The JSON controls layer order, offsets, mirroring,
rotation, scale, duration, looping, easing, and keyframes; the game interpolates it
at runtime. There are no pre-rendered frame sequences.

Generate missing files with:

```powershell
py games/castle_crashers_terrible_edition/tools/export_all_art.py
py games/castle_crashers_terrible_edition/tools/generate_rig_art.py
py games/castle_crashers_terrible_edition/tools/generate_cyclops_character_art.py
py games/castle_crashers_terrible_edition/tools/generate_missing_magic_art.py
py games/castle_crashers_terrible_edition/tools/export_background_art.py
py games/castle_crashers_terrible_edition/tools/audit_texture_coverage.py --write-manifest
```

Both generators preserve existing files by default. Use `--force` only when you
deliberately want to replace repainted artwork with the legacy vector version.

Runtime code may still rotate, flip, stretch, tint, or move these PNGs. Particles,
glow, weather, damage numbers, collision guides, health bars, and text remain
procedural because they are effects or interface feedback rather than source art.
`assets/texture_manifest.json` is the machine-checked list of source textures.
