#!/usr/bin/env python3
"""Convert portrait image to animated ASCII art SVG in Dark Neon Teal.

Matches dimensions and styling of info-card.svg (width: 370, height: 550).
Produces: hxni-ascii.svg (in project root)
"""

import os
import sys

from PIL import Image


def image_to_ascii(image_path, target_cols=72, target_rows=62):
    try:
        raw_img = Image.open(image_path)
        if raw_img.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", raw_img.size, (0, 0, 0))
            bg.paste(raw_img, mask=raw_img.split()[-1])
            img = bg.convert("L")
        else:
            img = raw_img.convert("L")
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        sys.exit(1)

    img = img.resize((target_cols, target_rows), Image.Resampling.LANCZOS)

    # Custom brightness-to-character density ramp
    chars = " .`:-=+*cs#%@"

    # Normalize brightness across non-black pixels to preserve face/suit details
    pixels = list(
        img.get_flattened_data()
        if hasattr(img, "get_flattened_data")
        else img.getdata()
    )

    # Find dynamic range of subject (ignoring pure black background)
    subject_pixels = [p for p in pixels if p > 5]
    if subject_pixels:
        min_p = min(subject_pixels)
        max_p = max(subject_pixels)
    else:
        min_p, max_p = 0, 255
    range_p = max(1, max_p - min_p)

    ascii_str = ""
    for pixel in pixels:
        if pixel <= 5:
            ascii_str += " "
        else:
            norm = (pixel - min_p) / range_p
            char_idx = int(norm * (len(chars) - 1))
            char_idx = max(0, min(len(chars) - 1, char_idx))
            ascii_str += chars[char_idx]

    ascii_lines = [
        ascii_str[i : i + target_cols] for i in range(0, len(ascii_str), target_cols)
    ]
    return ascii_lines


def generate_svg(ascii_lines, output_path):
    width = 370
    height = 550

    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <defs>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="1.0" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <style>
            .bg {{ fill: #0a0f0d; stroke: #1a2a2a; stroke-width: 2px; }}
            .text {{
                font-family: "Courier New", Consolas, "Liberation Mono", monospace;
                font-size: 7.4px;
                letter-spacing: 0.8px;
                fill: #00FFD1;
                filter: url(#glow);
            }}
            .title {{
                font-family: "Courier New", Consolas, monospace;
                font-size: 14px;
                font-weight: bold;
                fill: #E0E0E0;
                text-anchor: middle;
            }}
            .line-sep {{ stroke: #1a2a2a; stroke-width: 1px; }}
            .line {{ opacity: 0; animation: fin 0.35s forwards; }}
            @keyframes fin {{
                from {{ opacity: 0; transform: translateY(2px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
'''

    styles = []
    for i in range(len(ascii_lines)):
        delay = i * 0.015
        styles.append(f"            .l{i} {{ animation-delay: {delay:.3f}s; }}")

    svg_header += "\n".join(styles)
    svg_header += f'''
        </style>
    </defs>

    <!-- Background Card -->
    <rect class="bg" width="100%" height="100%" rx="12" />

    <!-- Terminal Header (matching info-card.svg) -->
    <g transform="translate(15, 20)">
        <circle cx="0" cy="0" r="6" fill="#FF5F56" />
        <circle cx="20" cy="0" r="6" fill="#FFBD2E" />
        <circle cx="40" cy="0" r="6" fill="#27C93F" />
    </g>
    <text x="185" y="25" class="title">furqanRupom.sh</text>
    <line x1="0" y1="40" x2="{width}" y2="40" class="line-sep" />

    <!-- ASCII Art Portrait -->
    <g transform="translate(185, 58)">
'''

    svg_lines = []
    line_step = 7.7
    for i, line in enumerate(ascii_lines):
        escaped_line = (
            line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        y_pos = i * line_step
        svg_lines.append(
            f'        <text x="0" y="{y_pos:.1f}" text-anchor="middle" class="text line l{i}">{escaped_line}</text>'
        )

    svg_footer = """    </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_header + "\n".join(svg_lines) + "\n" + svg_footer)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "source-prepped.png")
    output_path = os.path.join(base_dir, "hxni-ascii.svg")

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        print("Please run prep_photo.py first.")
        sys.exit(1)

    ascii_lines = image_to_ascii(input_path)
    generate_svg(ascii_lines, output_path)
    print(f"Success! Generated {output_path}")
