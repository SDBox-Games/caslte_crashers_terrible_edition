"""Generate the Parade cart body texture used by the runtime renderer."""

from pathlib import Path

from PIL import Image, ImageDraw


SCALE = 2
SIZE = (1120, 240)
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "story" / "parade_cart.png"


def box(draw, bounds, radius, fill, outline=None, width=1):
    scaled = tuple(int(value * SCALE) for value in bounds)
    draw.rounded_rectangle(
        scaled,
        radius=int(radius * SCALE),
        fill=fill,
        outline=outline,
        width=int(width * SCALE),
    )


def line(draw, points, fill, width):
    draw.line(
        [(int(x * SCALE), int(y * SCALE)) for x, y in points],
        fill=fill,
        width=int(width * SCALE),
        joint="curve",
    )


def main():
    image = Image.new("RGBA", (SIZE[0] * SCALE, SIZE[1] * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    ink = (32, 28, 34, 255)
    wood = (179, 105, 63, 255)
    dark_wood = (115, 70, 44, 255)
    deck_wood = (151, 91, 53, 255)
    trim = (225, 201, 129, 255)
    glass = (84, 156, 181, 255)
    glass_light = (150, 216, 226, 255)

    # Enclosed carriage room and its pale celebration roof.
    box(draw, (60, 22, 720, 212), 15, ink)
    box(draw, (72, 34, 708, 200), 11, wood)
    box(draw, (30, 1, 750, 39), 12, ink)
    box(draw, (41, 10, 739, 30), 8, trim)

    # Broad, readable wooden panels give the texture a hand-painted cart feel.
    for panel_x in (92, 242, 392, 542, 692):
        line(draw, ((panel_x, 42), (panel_x, 192)), (124, 73, 50, 255), 5)
    line(draw, ((78, 187), (702, 187)), (225, 143, 77, 255), 4)

    for window_x in (155, 305, 455, 605):
        box(draw, (window_x - 42, 65, window_x + 42, 153), 16, ink)
        box(draw, (window_x - 34, 73, window_x + 34, 145), 11, glass)
        line(draw, ((window_x - 23, 81), (window_x + 20, 137)), glass_light, 5)

    # The passenger deck is the front of the mirrored cart and faces right.
    box(draw, (700, 95, 1085, 207), 16, ink)
    box(draw, (710, 104, 1075, 196), 12, deck_wood)
    line(draw, ((722, 113), (1060, 113)), (235, 190, 72, 255), 7)
    for rail_x in (735, 820, 905, 990, 1060):
        line(draw, ((rail_x, 112), (rail_x, 158)), ink, 5)

    # A single long undercarriage ties the room and passenger deck together.
    box(draw, (30, 190, 1110, 228), 12, ink)
    box(draw, (41, 199, 1099, 219), 8, dark_wood)
    for bolt_x in range(80, 1090, 95):
        draw.ellipse(
            ((bolt_x - 4) * SCALE, 205 * SCALE, (bolt_x + 4) * SCALE, 213 * SCALE),
            fill=trim,
        )

    image = image.resize(SIZE, Image.Resampling.LANCZOS)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT)
    print(f"Generated {OUTPUT} ({SIZE[0]}x{SIZE[1]})")


if __name__ == "__main__":
    main()
