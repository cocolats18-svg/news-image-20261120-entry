#!/usr/bin/env python3
"""Generate entry.png for news-image-20261120 with Pillow (local only, not part of the entry).

Original layout for 20 November 2026 world news, adapted from the
newspaper-style pattern: banner with the date, one lead card, six story
cards and an "also on" strip. All text is drawn from the verified brief.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BG = (247, 243, 232)
NAVY = (15, 42, 68)
INK = (20, 24, 30)
RED = (178, 34, 34)
TEAL = (0, 110, 110)
GOLD = (198, 142, 0)
WHITE = (255, 255, 255)
GREY = (70, 75, 85)

def font(size, bold=True):
    path = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- top banner ---
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((36, 22), "THE WORLD IN ONE DAY", font=font(44), fill=WHITE)
d.text((36, 82), "FRIDAY  20  NOVEMBER  2026", font=font(34), fill=(255, 214, 90))
d.text((36, 122), "World news, summed up in one image", font=font(20, False), fill=(200, 215, 230))

def wrap_text(draw, text, fnt, max_w, x, y, fill, spacing=4, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line so an ellipsis fits
        while lines and draw.textlength(lines[-1] + "...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "..."
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

def card(x, y, w, h, accent, tag, headline, sub):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    d.rounded_rectangle([x, y, x + w, y + 34], radius=14, fill=accent)
    d.rectangle([x, y + 20, x + w, y + 34], fill=accent)
    d.text((x + 14, y + 6), tag, font=font(16), fill=WHITE)
    y2 = wrap_text(d, headline, font(21), w - 28, x + 14, y + 44, INK, max_lines=3)
    wrap_text(d, sub, font(15, False), w - 28, x + 14, y2 + 4, GREY, max_lines=3)

# --- lead story: missiles in Poland / NATO ---
lx, ly, lw, lh = 36, 168, 952, 218
d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=16, fill=WHITE,
                    outline=(210, 205, 190), width=2)
d.rounded_rectangle([lx, ly, lx + lw, ly + 40], radius=16, fill=RED)
d.rectangle([lx, ly + 26, lx + lw, ly + 40], fill=RED)
d.text((lx + 16, ly + 8), "LEAD  •  POLAND  /  NATO", font=font(19), fill=WHITE)
# warning icon: red disc with a white exclamation mark, plus gold ring
d.ellipse([lx + 42, ly + 66, lx + 122, ly + 146], fill=RED, outline=(255, 214, 90), width=4)
d.rectangle([lx + 77, ly + 80, lx + 87, ly + 118], fill=WHITE)
d.ellipse([lx + 77, ly + 126, lx + 87, ly + 136], fill=WHITE)
wrap_text(d, "Russian missiles land in Poland", font(33), 640, lx + 220, ly + 56, INK, max_lines=2)
wrap_text(d, "Two missiles and a suspected drone came down in Poland during a "
             "barrage on Ukraine. Warsaw calls it a deliberate provocation; "
             "NATO calls it a grave violation of its airspace.",
          font(19, False), 640, lx + 220, ly + 104, GREY, max_lines=3)

stories = [
    (TEAL, "UKRAINE", "Kyiv hit in overnight barrage; Ukraine strikes back",
     "Missiles batter Kyiv; Ukrainian drones hit the Dorogobuzh plant in Russia."),
    (NAVY, "SUMMIT AFTERMATH", "Shenzhen deal, but no breakthrough",
     "US, China and Russia issue a joint peace declaration. Merz: no new \u201cYalta\u201d without Europe."),
    (RED, "MYANMAR", "World court: Myanmar committed genocide",
     "ICJ rules 9-6: state-sponsored genocide against the Rohingya in Rakhine."),
    (GOLD, "MARKETS", "Stocks slide: S&P -3.7%, Nikkei -5.06%",
     "Sixth straight down day for the S&P as AI-cost fears hit; Anthropic slides after its record IPO."),
    (TEAL, "GULF", "Houthi strike hits Riyadh; tanker ablaze",
     "Missile hits the PIF Tower in Riyadh; an oil tanker is on fire in the Strait of Hormuz."),
    (NAVY, "EUROPE", "EU-UK deals in Brussels",
     "Food trade, carbon markets and youth mobility: 100,000 places each side, ages 18-31."),
]
cw, ch, gap = 304, 184, 20
for i, (accent, tag, head, sub) in enumerate(stories):
    x = 36 + (i % 3) * (cw + gap)
    y = 406 + (i // 3) * (ch + gap)
    card(x, y, cw, ch, accent, tag, head, sub)

# --- bottom strip ---
by = 406 + 2 * ch + gap + 18
d.rounded_rectangle([36, by, 988, by + 108], radius=14, fill=NAVY)
d.text((56, by + 12), "ALSO ON 20 NOVEMBER", font=font(19), fill=(255, 214, 90))
wrap_text(d, "Cyclone Akvan hits Odisha  \u2022  Kerch Bridge rail resumes  \u2022  Kenya counts down to Ebola-free  \u2022  BepiColombo reaches Mercury  \u2022  Peru quake 6.7  \u2022  Sheinbaum's 21-hour economy flight",
          font(18, False), 900, 56, by + 44, WHITE, max_lines=3)
d.text((36, 968), "Events reported on 20 November 2026  \u2022  One day, one image",
       font=font(16, False), fill=(110, 110, 110))

out = "/home/hatch/workspace/bountyhawk/news-image-20261120-entry/entry.png"
img.save(out, optimize=True)
print("saved", img.size)
print(os.path.getsize(out))
