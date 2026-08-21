# -*- coding: utf-8 -*-
"""One-off prep: crops the source logo artwork down to logo_full.png
(mark + tagline + phone) and logo_mark.png (mark only, for small use).
Re-run this only if the source logo file changes; point SOURCE_LOGO at
wherever the new file was saved, then also re-run quantize (see README)."""
import os
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_LOGO = r"C:\Users\User\Pictures\Logo-02.png"

im = Image.open(SOURCE_LOGO).convert("RGB")
print("size", im.size)

bg = Image.new("RGB", im.size, (255, 255, 255))
diff = ImageChops.difference(im, bg)
# threshold: treat near-white as background
gray = diff.convert("L").point(lambda p: 255 if p > 10 else 0)
bbox = gray.getbbox()
print("bbox", bbox)

pad = 14
l, t, r, b = bbox
l = max(0, l - pad); t = max(0, t - pad)
r = min(im.width, r + pad); b = min(im.height, b + pad)
crop = im.crop((l, t, r, b))
crop.save(os.path.join(HERE, "logo_full.png"))
print("cropped size", crop.size)

cw, ch = crop.size
cbg = Image.new("RGB", crop.size, (255, 255, 255))
cdiff = ImageChops.difference(crop, cbg)
cgray = cdiff.convert("L").point(lambda p: 255 if p > 10 else 0)

# scan rows for a wide white gap (split between the mark and the tagline text block)
row_has_content = []
px = cgray.load()
for y in range(ch):
    has = any(px[x, y] for x in range(0, cw, 3))
    row_has_content.append(has)

run = 0
gap_start = None
split_row = None
for y in range(ch):
    if not row_has_content[y]:
        run += 1
        if run > 10 and gap_start is None and y > ch * 0.35:
            gap_start = y - run + 1
    else:
        if gap_start is not None and split_row is None:
            split_row = gap_start
        run = 0
print("split_row", split_row, "of", ch)

mark_bottom = split_row if split_row else int(ch * 0.72)
mark = crop.crop((0, 0, cw, mark_bottom))
mbg = Image.new("RGB", mark.size, (255, 255, 255))
mdiff = ImageChops.difference(mark, mbg)
mgray = mdiff.convert("L").point(lambda p: 255 if p > 10 else 0)
mbbox = mgray.getbbox()
ml, mt, mr, mb = mbbox
mark2 = mark.crop((max(0, ml - 8), max(0, mt - 8), min(mark.width, mr + 8), min(mark.height, mb + 8)))
mark2.save(os.path.join(HERE, "logo_mark.png"))
print("mark size", mark2.size)

# Quantize to a small palette for the web-embedded copies build_catalog.py
# uses — this flat-color artwork compresses to well under half the size
# with no visible loss.
for name in ("logo_full", "logo_mark"):
    src = Image.open(os.path.join(HERE, name + ".png")).convert("RGB")
    src.quantize(colors=32, method=Image.MEDIANCUT).save(
        os.path.join(HERE, name + "_q.png"), optimize=True)
print("wrote logo_full_q.png, logo_mark_q.png")
