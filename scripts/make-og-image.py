#!/usr/bin/env python3
"""Generate the default 1200x630 Open Graph preview card (images/og-image.png).

Adapted from upstream AcademicPages scripts/make-og-image.py and customized for
Roberto M. Fuentes's academic portfolio (https://fuentes-rm.github.io).

Usage:
    python3 scripts/make-og-image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, H = 1200, 630
BG = (255, 255, 255)          # clean white background
NAVY = (24, 54, 96)           # deep academic navy accent
BLUE = (42, 98, 178)          # primary accent blue
DARK = (34, 41, 47)           # primary text
GREY = (92, 104, 115)         # secondary text
LIGHTBLUE = (236, 243, 252)   # pill background
BORDER = (222, 230, 240)      # subtle divider/border

FONT_DIR = os.environ.get("FONT_DIR", "/usr/share/fonts/truetype/dejavu")


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    p = os.path.join(FONT_DIR, name)
    if not os.path.exists(p):
        p = os.path.join(
            "/usr/share/fonts/truetype/liberation",
            "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
        )
    return ImageFont.truetype(p, size)


def paste_circular_avatar(base_img, avatar_path, box_xy, diameter):
    avatar = Image.open(avatar_path).convert("RGB")
    # Crop square centered toward top (matching CSS object-position: center top)
    w, h = avatar.size
    side = min(w, h)
    left = (w - side) // 2
    top = 0 if h > w else (h - side) // 2
    avatar = avatar.crop((left, top, left + side, top + side))
    avatar = avatar.resize((diameter, diameter), Image.Resampling.LANCZOS)

    mask = Image.new("L", (diameter, diameter), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, diameter - 1, diameter - 1), fill=255)

    # Subtle circular ring
    ring_pad = 6
    ring_diam = diameter + ring_pad * 2
    draw = ImageDraw.Draw(base_img)
    rx, ry = box_xy[0] - ring_pad, box_xy[1] - ring_pad
    draw.ellipse((rx, ry, rx + ring_diam, ry + ring_diam), fill=(255, 255, 255), outline=BORDER, width=3)
    base_img.paste(avatar, box_xy, mask)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Top accent bar
    d.rectangle([0, 0, W, 12], fill=NAVY)

    f_title = font(56, bold=True)
    f_role = font(30, bold=True)
    f_sub = font(27)
    f_pill = font(24, bold=True)
    f_domain = font(26, bold=True)

    # Circular profile photo (top-right) if available, fallback to academic favicon
    profile_path = os.path.join(REPO_ROOT, "images", "profile.jpg")
    logo_path = os.path.join(REPO_ROOT, "images", "favicon-512x512.png")
    if os.path.exists(profile_path):
        paste_circular_avatar(img, profile_path, (W - 220 - 70, 56), 220)
    elif os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((200, 200), Image.Resampling.LANCZOS)
        img.paste(logo, (W - 200 - 70, 56), logo)

    # Name, affiliation, and research summary
    d.text((70, 62), "Roberto M. Fuentes", font=f_title, fill=DARK)
    d.text((70, 142), "Researcher · University of Talca", font=f_role, fill=BLUE)
    d.text((70, 206), "Control Theory, Uncertain Sampled-Data Systems,", font=f_sub, fill=GREY)
    d.text((70, 248), "and Markov Jump Linear Systems", font=f_sub, fill=GREY)

    # Divider
    d.line([70, 344, W - 70, 344], fill=BORDER, width=2)

    # Topic / section pills
    pills = ["Publications", "Control Theory", "Teaching", "People", "CV"]
    x = 70
    y = 392
    for label in pills:
        fw = int(d.textlength(label, font=f_pill)) + 44
        if x + fw > W - 70:
            x = 70
            y += 70
        d.rounded_rectangle([x, y, x + fw, y + 54], radius=27, fill=LIGHTBLUE, outline=BORDER, width=1)
        d.text((x + 22, y + 12), label, font=f_pill, fill=NAVY)
        x += fw + 16

    # Footer domain badge
    domain = "fuentes-rm.github.io"
    dw = int(d.textlength(domain, font=f_domain)) + 64
    d.rounded_rectangle([70, H - 96, 70 + dw, H - 44], radius=26, fill=NAVY)
    d.text((102, H - 86), domain, font=f_domain, fill=(255, 255, 255))

    out = os.path.join(REPO_ROOT, "images", "og-image.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", os.path.normpath(out), img.size)


if __name__ == "__main__":
    main()
