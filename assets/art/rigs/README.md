# JSON part-animation rigs

Each folder is one animated actor:

```text
rigs/<actor>/
  animation.json
  parts/
    body.png
    head.png
    hand_1.png
    ...
```

Part PNGs use a transparent canvas whose center is the rotation pivot. The game
automatically removes excess transparent padding in memory while keeping that
pivot fixed.

An animation contains `duration`, `loop`, and an ordered `layers` list. Layers
are painted back-to-front and support:

- `part`: PNG filename without `.png`
- `offset`: `[x, y]` from the actor origin
- `rotation`: base rotation in degrees
- `scale`: base scale for the part
- `mirror`: horizontally mirror this layer
- `ease`: `smooth` (default) or `linear`
- `keyframes`: timed `x`, `y`, `rotation`, `scale_x`, and `scale_y` values

The renderer interpolates between keyframes. Looping animations should include a
final keyframe at `time == duration` matching their first pose so the loop closes
cleanly. Edit JSON while the game is closed, then relaunch to reload it.
