"""
Generates game/gui/chat/phone_frame_app.png, the phone frame used for the
dating app, from the normal messaging frame game/gui/chat/phone_frame.png.

The blue header bar is recolored into a coral-to-pink gradient. Only the hue
changes, so the anti-aliased edges, the camera dot and the white icons keep
their shape.

Needs Pillow. Run from the project root:

    python3 tools/make_phone_frames.py
"""

import colorsys
import os

from PIL import Image

CHAT = os.path.join(os.path.dirname(__file__), "..", "game", "gui", "chat")

# The header bar is above this line; the chat area starts right below it.
HEADER_BOTTOM = 130

# Hue (in degrees) at the left and right edges of the header.
HUE_LEFT = 8
HUE_RIGHT = 335


def gradient_hue(x, width):
    # Go from HUE_LEFT down through red to HUE_RIGHT, the short way round.
    span = (HUE_LEFT - HUE_RIGHT) % 360
    return ((HUE_LEFT - span * x / (width - 1)) % 360) / 360.0


def main():
    im = Image.open(os.path.join(CHAT, "phone_frame.png")).convert("RGBA")
    px = im.load()
    width, _ = im.size

    for y in range(HEADER_BOTTOM):
        for x in range(width):
            r, g, b, a = px[x, y]
            if not a:
                continue

            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

            # Blue pixels of the bar (and its edges); leave grays alone.
            if s < 0.08 or not (0.5 < h < 0.7):
                continue

            r, g, b = colorsys.hsv_to_rgb(gradient_hue(x, width), min(1.0, s * 1.1), v)
            px[x, y] = (int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5), a)

    im.save(os.path.join(CHAT, "phone_frame_app.png"))


if __name__ == "__main__":
    main()
