"""
Generate a proper multi-size .ico file for JustDownloadIT.
Icon design: Rounded blue square (ACCENT #3aa0ff) with a white download arrow
(arrow + tray) — matches the app's existing logo palette (see _draw_logo in
JustDownloadIT.py). Produces all standard sizes inside one .ico file so
Windows picks the correct size for taskbar, desktop shortcut, small icons,
large icons, Add/Remove Programs etc.
"""
from PIL import Image, ImageDraw

ACCENT = "#3aa0ff"
ACCENT_DARK = "#2b88e0"
WHITE = "#ffffff"
BLUE_LIGHT = "#eaf4ff"

SIZES = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]

def make_icon(size):
    """Return a RGBA Image of one icon variant."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # ---- Rounded square base (ACCENT blue fill, ACCENT_DARK border) ----
    radius = max(2, size // 5)
    pad = max(1, size // 32)
    border_w = max(1, size // 48)
    # background fill body
    d.rounded_rectangle(
        [pad, pad, size - 1 - pad, size - 1 - pad],
        radius=radius,
        fill=ACCENT,
    )
    # darker bottom shade for depth
    shade_h = size // 5
    d.rounded_rectangle(
        [pad, size - 1 - pad - shade_h, size - 1 - pad, size - 1 - pad],
        radius=radius,
        fill=ACCENT_DARK,
    )
    # clean corners of shade-only top
    d.rounded_rectangle(
        [pad, pad, size - 1 - pad, size - 1 - pad - shade_h + radius // 2],
        radius=radius,
        fill=ACCENT,
    )
    # border line
    d.rounded_rectangle(
        [pad, pad, size - 1 - pad, size - 1 - pad],
        radius=radius,
        outline=ACCENT_DARK,
        width=border_w,
    )

    # ---- Download arrow (white) ----
    # Layout: arrow in upper-middle, pointing down to a tray/bar near bottom
    # Scale all geometry off 'size'
    cx = size / 2
    # Arrow head dimensions
    aw = size * 0.38      # arrow head total width
    ah = size * 0.22      # arrow head height (triangle)
    shaft_w = size * 0.12
    shaft_h = size * 0.22
    shaft_top = size * 0.18
    tray_top = size * 0.72
    tray_h = size * 0.10
    tray_w = size * 0.56
    tray_left = cx - tray_w / 2
    tray_right = cx + tray_w / 2
    tray_bottom = size * 0.83

    # Shaft (vertical rectangle)
    d.rectangle(
        [cx - shaft_w / 2, shaft_top, cx + shaft_w / 2, shaft_top + shaft_h],
        fill=WHITE,
    )
    # Arrowhead (isosceles triangle, base DOWN)
    ah_top = shaft_top + shaft_h
    ah_bottom = ah_top + ah
    d.polygon(
        [
            (cx - aw / 2, ah_top),
            (cx + aw / 2, ah_top),
            (cx, ah_bottom),
        ],
        fill=WHITE,
    )
    # Tray (thick horizontal rectangle with slightly rounded caps via draw.rect + small triangle/rounding mask)
    tray_radius = max(1, int(size * 0.03))
    d.rounded_rectangle(
        [tray_left, tray_top, tray_right, tray_top + tray_h],
        radius=tray_radius,
        fill=WHITE,
    )

    # Anti-alias pass: render at 2x then downscale for sizes <= 64
    if size <= 64:
        big = make_icon_native(size * 2)
        return big.resize((size, size), Image.LANCZOS)
    return img


def make_icon_native(size):
    """Internal copy without the recursive resize step."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = max(2, size // 5)
    pad = max(1, size // 32)
    border_w = max(1, size // 48)
    d.rounded_rectangle([pad, pad, size - 1 - pad, size - 1 - pad], radius=radius, fill=ACCENT)
    shade_h = size // 5
    d.rounded_rectangle([pad, size - 1 - pad - shade_h, size - 1 - pad, size - 1 - pad], radius=radius, fill=ACCENT_DARK)
    d.rounded_rectangle([pad, pad, size - 1 - pad, size - 1 - pad - shade_h + radius // 2], radius=radius, fill=ACCENT)
    d.rounded_rectangle([pad, pad, size - 1 - pad, size - 1 - pad], radius=radius, outline=ACCENT_DARK, width=border_w)

    cx = size / 2
    aw = size * 0.38; ah = size * 0.22
    shaft_w = size * 0.12; shaft_h = size * 0.22
    shaft_top = size * 0.18
    tray_h = size * 0.10; tray_w = size * 0.56
    tray_left = cx - tray_w / 2; tray_right = cx + tray_w / 2
    tray_top = size * 0.72

    d.rectangle([cx - shaft_w / 2, shaft_top, cx + shaft_w / 2, shaft_top + shaft_h], fill=WHITE)
    ah_top = shaft_top + shaft_h
    ah_bottom = ah_top + ah
    d.polygon([(cx - aw / 2, ah_top), (cx + aw / 2, ah_top), (cx, ah_bottom)], fill=WHITE)
    tray_radius = max(1, int(size * 0.03))
    d.rounded_rectangle([tray_left, tray_top, tray_right, tray_top + tray_h], radius=tray_radius, fill=WHITE)
    return img


# Build list of PIL images: sizes from largest to smallest to work around PIL save ordering
images = [make_icon(s) for s in SIZES]

out = r"d:\Projects\Yt video Downloader\app_icon.ico"
# PIL save with sizes= forces multi-size ICO
images[0].save(
    out,
    format="ICO",
    sizes=[(s, s) for s in SIZES],
    append_images=images[1:],
)

print(f"Wrote {out} with sizes: {SIZES}")
