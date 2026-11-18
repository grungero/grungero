"""Print-on-demand PNGs (Redbubble / Teepublic): transparent, trimmed, 4500x5400.

Usage: python3 pod.py <out_dir>
"""
import os
import sys

from PIL import Image

import wallart

wallart.TRANSPARENT = True
OUT_W, OUT_H = 4500, 5400  # standard apparel canvas; Redbubble scales for stickers/mugs/posters
PAD = 150

NAMES_ABSTRACT = ["boho-arches-sun", "boho-rainbow", "sun-over-hills", "botanical-stem", "stacked-sun-shapes", "boho-sun-rays"]
NAMES_AFFIRM = ["slow-down-right-on-time", "grow-at-your-own-pace", "soft-heart-strong-roots",
                "this-too-is-a-beginning", "rest-is-part-of-the-work", "be-where-your-feet-are"]


def fit(img):
    bbox = img.getbbox()
    img = img.crop(bbox)
    scale = min((OUT_W - 2 * PAD) / img.width, (OUT_H - 2 * PAD) / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    out = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    out.paste(img, ((OUT_W - img.width) // 2, (OUT_H - img.height) // 2), img)
    return out


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for i, n in enumerate(NAMES_ABSTRACT):
        fit(wallart.abstract(i, 3000, 4500)).save(os.path.join(out_dir, f"{n}.png"), optimize=True)
        print(n)
    for i, n in enumerate(NAMES_AFFIRM):
        fit(wallart.affirmation(i, 3000, 4500)).save(os.path.join(out_dir, f"{n}.png"), optimize=True)
        print(n)


if __name__ == "__main__":
    main(sys.argv[1])


def dark_variants(out_dir):
    """Affirmations with cream text, for dark garments (black, navy, forest, charcoal)."""
    wallart.PAL["ink"] = "#F3ECE2"
    for i, n in enumerate(NAMES_AFFIRM):
        fit(wallart.affirmation(i, 3000, 4500)).save(os.path.join(out_dir, f"{n}-DARK-SHIRTS.png"), optimize=True)
    wallart.PAL["ink"] = "#3D3530"
