"""Split the two transparent generated atlases into gameplay sprites.

Run with ``py extract_cast.py`` after replacing either versioned atlas. The
splitter finds the four large alpha components, so it does not depend on the
image generator returning a perfectly divisible canvas width.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


APP_DIR = Path(__file__).resolve().parent
GENERATED_DIR = APP_DIR / "assets" / "generated"
OUTPUT_DIR = GENERATED_DIR / "cast"
ATLASES = (
    (
        GENERATED_DIR / "knights_atlas_v2.png",
        ("ember", "tide", "grove", "storm"),
    ),
    (
        GENERATED_DIR / "story_cast_atlas_v2.png",
        ("barbarian", "cheese_boss", "king", "royal_guard"),
    ),
)


def trim(image: np.ndarray, padding: int = 10) -> np.ndarray:
    points = cv2.findNonZero((image[:, :, 3] > 0).astype("uint8"))
    if points is None:
        return image
    x, y, width, height = cv2.boundingRect(points)
    left, top = max(0, x - padding), max(0, y - padding)
    right = min(image.shape[1], x + width + padding)
    bottom = min(image.shape[0], y + height + padding)
    return image[top:bottom, left:right]


def split_atlas(path: Path, names: tuple[str, ...]) -> None:
    atlas = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if atlas is None or atlas.ndim != 3 or atlas.shape[2] != 4:
        raise SystemExit(f"{path} must be an RGBA image")
    alpha_mask = (atlas[:, :, 3] > 10).astype("uint8")
    count, labels, stats, centers = cv2.connectedComponentsWithStats(alpha_mask, 8)
    major_labels = sorted(
        range(1, count), key=lambda label: int(stats[label, cv2.CC_STAT_AREA]), reverse=True
    )[: len(names)]
    if len(major_labels) != len(names):
        raise SystemExit(f"Expected {len(names)} characters in {path}")
    major_labels.sort(key=lambda label: float(centers[label][0]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, major_label in zip(names, major_labels):
        # Keep the exact major alpha island. Generated cast members occasionally
        # sit only one pixel apart, so dilation or nearest-effect assignment can
        # accidentally pull a neighbor's shield into the crop.
        region = (labels == major_label).astype("uint8")
        output = atlas.copy()
        output[:, :, 3] = np.where(region > 0, atlas[:, :, 3], 0)
        output = trim(output)
        destination = OUTPUT_DIR / f"{name}.png"
        if not cv2.imwrite(str(destination), output):
            raise SystemExit(f"Could not save {destination}")


def main() -> None:
    for path, names in ATLASES:
        split_atlas(path, names)
    print(f"Extracted 8 transparent gameplay sprites to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
