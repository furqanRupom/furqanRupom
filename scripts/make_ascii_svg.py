#!/usr/bin/env python3
import os
import sys

from PIL import Image


def image_to_ascii(image_path, new_width=75):
    try:
        img = Image.open(image_path).convert("L")
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        sys.exit(1)

    width, height = img.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55
    )  # 0.55 corrects character aspect ratio
    img = img.resize((new_width, new_height))

    pixels = img.getdata()
    chars = " .:-=+*cs#%@"

    ascii_str = ""
    for pixel in pixels:
        # map 0-255 to 0-len(chars)-1
        char_idx = int((pixel / 255.0) * (len(chars) - 1))
        ascii_str += chars[char_idx]

    ascii_img = [
        ascii_str[index : index + new_width]
        for index in range(0, len(ascii_str), new_width)
    ]
    return ascii_img


def generate_svg(ascii_lines, output_path):
    width = 370
    # Calculate height based on lines
    height = max(550, len(ascii_lines) * 7 + 40)

    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <defs>
        <filter id="glow">
            <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <style>
            .bg {{ fill: #0d0d0d; rx: 12px; stroke: #1a2a2a; stroke-width: 2px; }}
            .text {{
                font-family: "Courier New", monospace;
                font-size: 6px;
                fill: #00FFD1;
                white-space: pre;
                filter: url(#glow);
            }}
            .line {{ opacity: 0; animation: fadeIn 0.5s forwards; }}
            @keyframes fadeIn {{
                to {{ opacity: 1; }}
            }}
'''

    styles = []
    for i in range(len(ascii_lines)):
        delay = i * 0.03
        styles.append(f"            .l{i} {{ animation-delay: {delay}s; }}")

    svg_header += "\n".join(styles)
    svg_header += """
        </style>
    </defs>
    <rect class="bg" width="100%" height="100%" />
    <g transform="translate(10, 20)">
"""

    svg_lines = []
    for i, line in enumerate(ascii_lines):
        # Escape XML chars
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y_pos = i * 7
        svg_lines.append(
            f'        <text x="0" y="{y_pos}" class="text line l{i}">{line}</text>'
        )

    svg_footer = """
    </g>
</svg>"""

    with open(output_path, "w") as f:
        f.write(svg_header + "\n".join(svg_lines) + svg_footer)


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
