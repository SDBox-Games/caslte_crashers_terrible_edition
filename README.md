# Caslte Crashers: Terrible Edition

An original controller-first medieval brawler prototype for SDBOX.

## Current slice

- Fullscreen main menu with cached, smoothly crossfading pictures
- Four-player `Press A to Join` character lobby
- Independent character selection for every joined controller
- Keyboard player support through `Enter to Join`
- Animation-ready segmented rigs for Electric, Ice, Fire, Green, Barbarian, Cheese Moon, King, and Royal Guard
- Enemy characters are selectable and playable in the same lobby as the knights
- Moving world-map party with Home Castle, Blacksmith, and Arena
- Arena PvP in multiplayer and an infinite enemy horde in single-player
- Blacksmith yard with separate Pet House and Weapon Frog interiors
- Touch a pet or weapon once to permanently unlock and equip it for that character
- Per-SDBOX-user, per-character JSON saves for equipment, pets, level unlocks, completions, and deaths
- Silent Home Castle theft animation: wand pull, crystal jump, escape, then the selected party emerges
- Reference-informed Home Castle throne hall with the raised king, door beneath, fallen guards, stools, windows, banner, and scrolling Barbarian waves
- The throne door enters a compact target-and-tables training room
- Pets use standalone transparent PNGs and smoothly trail their owning player
- Knocked-out co-op players can be revived with Y; a complete party wipe returns to the map
- Home Castle completion unlocks the Blacksmith and Arena for every participating character
- Every level and interior uses the same JSON-driven scene, camera, door, pickup, and combat runtime
- Optional per-screen music from the `audio` folder

## Controls

- Character lobby: A joins a controller; Enter joins the keyboard
- Character lobby: D-pad Up/Down changes knight; A confirms; B cancels/leaves
- D-pad / left stick: navigate or move
- A: accept, interact, or attack
- Y: revive a nearby knocked-out player (keyboard: Y or K)
- B: close a menu; it never exits a level or the map directly
- Start: open the level/map menu (Resume, Return to Map/Main Menu)
- Keyboard: arrows/WASD, Enter, Z/J/Space, Y/K, Escape, P

## Custom assets

- Add menu pictures to `pictures/main_menu`. They are loaded once at startup, scaled to fill, then crossfaded without reloading every frame.
- Add `main_menu.mp3`, `map.mp3`, `arena.mp3`, `blacksmith.mp3`, or `home_castle.mp3` to `audio`. OGG and WAV also work.
- Level data lives in `levels/*.json`. A scene can define its world width, bounds, background, doors, waves, pets, and weapons.
- Every rig part is independent: `head.png`, `body.png`, `arm_left.png`, `arm_right.png`, `leg_left.png`, and `leg_right.png` under `assets/characters/<character>`.
- Custom rigs may use `left_arm.png`, `right_arm.png`, `left_leg.png`, and `right_leg.png`; the loader supports both naming styles. Electric also falls back through `electric/`, `electricity/`, then legacy `ember/`.
- Every weapon/wand is an independent transparent file in `assets/weapons`; every pet is an independent transparent file in `assets/pets`.
- Generated cast atlases and extracted portrait sprites live in `assets/generated`.
- Run `py extract_cast.py` after replacing a versioned generated atlas.
- Run `py generate_modular_assets.py` to rebuild the included non-custom rig parts, weapons, and pets. It deliberately does not overwrite the custom Electric folder.
- Run `py generate_assets.py` to rebuild the older menu scenes.

Run from SDBOX or directly with:

```powershell
py games\castle_crashers_terrible_edition\main.py
```
