"""Generate printable boho wall art sets in multiple print ratios.

Usage: python3 wallart.py <out_dir>
Creates two sets (affirmations + abstract arches), 6 designs each, 5 ratios each, at 300 DPI.
"""
import math
import os
import random
import sys
import zipfile

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/crosextra/"
PAL = dict(cream="#F3ECE2", sand="#E3D3BE", clay="#C9825F", rust="#A85A3C", sage="#9AA58C",
           olive="#6F7556", blush="#E2B8A6", ink="#3D3530", mustard="#D3A54A")
# ratio name -> (w_in, h_in) largest common print size for that ratio
RATIOS = {"2x3": (16, 24), "3x4": (18, 24), "4x5": (16, 20), "11x14": (11, 14), "ISO-A": (16.54, 23.39)}
DPI = 300
BASE_W, BASE_H = 2000, 3000  # design canvas (2:3); each ratio re-composes on its own canvas

AFFIRMATIONS = [
    ("Slow down,", "you're right on time."),
    ("Grow at", "your own pace."),
    ("Soft heart,", "strong roots."),
    ("This, too,", "is a beginning."),
    ("Rest is", "part of the work."),
    ("Be where", "your feet are."),
]


def font(name, size):
    return ImageFont.truetype(FONT + name, size)


def arch(d, cx, base_y, w, h, fill):
    r = w / 2
    d.rectangle([cx - r, base_y - h + r, cx + r, base_y], fill=fill)
    d.pieslice([cx - r, base_y - h, cx + r, base_y - h + 2 * r], 180, 360, fill=fill)


def rainbow(d, cx, cy, radii, colors, thick):
    for r, c in zip(radii, colors):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=c, width=thick)


def sun(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def half_sun(d, cx, cy, r, fill):
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=fill)


def leaf(d, x, y, length, angle, fill):
    pts = []
    for t in range(0, 101):
        u = t / 100
        wdt = math.sin(math.pi * u) * length * 0.22
        pts.append((u * length, wdt))
    pts += [(p[0], -p[1]) for p in reversed(pts)]
    a = math.radians(angle)
    d.polygon([(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts], fill=fill)


def stem(d, x, y, length, angle, color, n=6):
    a = math.radians(angle)
    ex, ey = x + length * math.cos(a), y + length * math.sin(a)
    d.line([x, y, ex, ey], fill=color, width=10)
    for i in range(1, n + 1):
        t = i / (n + 1)
        px, py = x + (ex - x) * t, y + (ey - y) * t
        leaf(d, px, py, length * 0.28, angle - 45, color)
        leaf(d, px, py, length * 0.28, angle + 45, color)


def grain(img, amount=10, seed=0):
    rnd = random.Random(seed)
    noise = Image.effect_noise(img.size, amount).convert("L")
    noise = noise.point(lambda v: 128 + (v - 128) // 3)
    overlay = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, Image.composite(img, overlay, Image.new("L", img.size, 235)), 0.25 + rnd.random() * 0.01)


# ---------- design functions draw on a W x H canvas ----------
def abstract(i, W, H):
    img = Image.new("RGB", (W, H), PAL["cream"])
    d = ImageDraw.Draw(img)
    u = min(W, H)
    cx = W / 2
    if i == 0:  # arches
        arch(d, cx - u * 0.12, H * 0.78, u * 0.5, H * 0.5, PAL["clay"])
        arch(d, cx + u * 0.14, H * 0.78, u * 0.36, H * 0.36, PAL["sage"])
        sun(d, cx + u * 0.2, H * 0.27, u * 0.09, PAL["mustard"])
    elif i == 1:  # rainbow
        rainbow(d, cx, H * 0.62, [u * 0.38, u * 0.29, u * 0.2, u * 0.11],
                [PAL["clay"], PAL["blush"], PAL["sage"], PAL["mustard"]], int(u * 0.08))
    elif i == 2:  # sun over hills
        m = u * 0.12
        sun(d, cx, H * 0.4, u * 0.17, PAL["clay"])
        half_sun(d, cx - u * 0.13, H * 0.66, u * 0.25, PAL["sage"])
        half_sun(d, cx + u * 0.15, H * 0.66, u * 0.2, PAL["olive"])
        d.rectangle([cx - u * 0.38, H * 0.66, cx + u * 0.38, H * 0.66 + u * 0.03], fill=PAL["sand"])
    elif i == 3:  # botanical stem
        stem(d, cx, H * 0.8, H * 0.55, -90, PAL["olive"], 5)
        sun(d, cx, H * 0.17, u * 0.05, PAL["clay"])
    elif i == 4:  # stacked shapes
        d.rectangle([cx - u * 0.3, H * 0.6, cx + u * 0.3, H * 0.8], fill=PAL["sand"])
        half_sun(d, cx, H * 0.6, u * 0.3, PAL["rust"])
        sun(d, cx, H * 0.32, u * 0.11, PAL["mustard"])
        d.ellipse([cx - u * 0.04, H * 0.84, cx + u * 0.04, H * 0.84 + u * 0.08], fill=PAL["sage"])
    else:  # sun rays
        sun(d, cx, H * 0.5, u * 0.16, PAL["clay"])
        for k in range(16):
            a = math.radians(k * 22.5)
            r1, r2 = u * 0.22, u * 0.36
            d.line([cx + r1 * math.cos(a), H * 0.5 + r1 * math.sin(a), cx + r2 * math.cos(a), H * 0.5 + r2 * math.sin(a)],
                   fill=PAL["mustard"], width=int(u * 0.018))
    return grain(img, seed=i)


def affirmation(i, W, H):
    img = Image.new("RGB", (W, H), PAL["cream"])
    d = ImageDraw.Draw(img)
    u = min(W, H)
    cx = W / 2
    accents = [PAL["clay"], PAL["sage"], PAL["blush"], PAL["mustard"], PAL["sand"], PAL["olive"]]
    acc = accents[i]
    # decorative motif upper part
    m = i % 3
    if m == 0:
        half_sun(d, cx, H * 0.42, u * 0.3, acc)
    elif m == 1:
        arch(d, cx, H * 0.46, u * 0.42, H * 0.3, acc)
    else:
        rainbow(d, cx, H * 0.44, [u * 0.3, u * 0.22, u * 0.14], [acc, PAL["clay"], PAL["sage"]], int(u * 0.055))
    l1, l2 = AFFIRMATIONS[i]
    f1 = font("Caladea-Italic.ttf", int(u * 0.095))
    f2 = font("Caladea-Regular.ttf", int(u * 0.095))
    y = H * 0.56
    for txt, f in ((l1, f1), (l2, f2)):
        size = f.size
        while d.textlength(txt, font=f) > W * 0.82:
            size -= 4
            f = font(f.path.split("/")[-1], size)
        d.text((cx, y), txt, font=f, fill=PAL["ink"], anchor="mt")
        y += size * 1.25
    d.line([cx - u * 0.06, y + u * 0.04, cx + u * 0.06, y + u * 0.04], fill=acc, width=int(u * 0.008))
    return grain(img, seed=10 + i)


SETS = {
    "boho-abstract": ("Boho Abstract Set of 6", abstract),
    "boho-affirmations": ("Boho Affirmation Set of 6", affirmation),
}


def export(out_dir):
    for slug, (name, fn) in SETS.items():
        sdir = os.path.join(out_dir, slug)
        os.makedirs(sdir, exist_ok=True)
        previews = []
        for rname, (wi, hi) in RATIOS.items():
            zpath = os.path.join(sdir, f"{slug}-{rname}.zip")
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_STORED) as z:
                for i in range(6):
                    W, H = int(wi * DPI), int(hi * DPI)
                    img = fn(i, W, H)
                    tmp = os.path.join(sdir, f"_tmp.jpg")
                    img.save(tmp, "JPEG", quality=90, dpi=(DPI, DPI), optimize=True)
                    z.write(tmp, f"{slug}-{i+1}-{rname}-{wi}x{hi}in.jpg")
                    if rname == "2x3":
                        previews.append(img.resize((800, 1200), Image.LANCZOS))
            os.remove(tmp)
            print(zpath, os.path.getsize(zpath) // 1024, "KB")
        pdir = os.path.join(sdir, "preview")
        os.makedirs(pdir, exist_ok=True)
        for i, p in enumerate(previews):
            p.save(os.path.join(pdir, f"{i+1}.jpg"), quality=88)


if __name__ == "__main__":
    export(sys.argv[1])
